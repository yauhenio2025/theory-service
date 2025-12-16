"""
LLM Clustering Service for Challenge Reconciliation.

Uses Claude Opus 4.5 with extended thinking to:
1. Group similar challenges from multiple projects
2. Identify consensus and contradictions
3. Generate recommendations for batch resolution
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime

from anthropic import Anthropic
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import (
    Challenge, EmergingConcept, EmergingDialectic,
    ChallengeCluster, ChallengeClusterMember,
    Concept, Dialectic,
    ClusterType, ClusterStatus, RecommendedAction, ChallengeStatus, EmergingStatus
)


# Claude configuration
CLAUDE_MODEL = "claude-sonnet-4-5-20250929"  # Using Sonnet for speed, Opus for deep analysis
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")


def get_anthropic_client():
    """Get Anthropic client."""
    if not ANTHROPIC_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")
    return Anthropic(api_key=ANTHROPIC_API_KEY)


CLUSTERING_SYSTEM_PROMPT = """You are an expert at analyzing theoretical challenges from empirical research.

Your task is to analyze a set of challenges to theoretical concepts or dialectics, identify patterns, and recommend resolutions.

For each set of challenges you receive:
1. Group truly similar challenges (same insight, different evidence sources)
2. Identify contradictions (challenges that conflict with each other)
3. Assess consensus strength (how many independent sources agree)
4. Recommend an action: accept (strong consensus), reject (weak/contradicted), human_review (complex/nuanced)

Output your analysis as JSON with this structure:
{
  "clusters": [
    {
      "summary": "One sentence describing what unifies this cluster",
      "challenge_ids": [list of challenge IDs in this cluster],
      "consensus_strength": "strong|moderate|weak",
      "recommendation": "accept|reject|human_review",
      "recommendation_rationale": "Why this recommendation",
      "contradictions_noted": ["Any contradictions within or against this cluster"]
    }
  ],
  "overall_assessment": "Brief summary of the theoretical implications"
}"""


async def cluster_concept_challenges(
    db: AsyncSession,
    concept_id: int,
    concept_term: str
) -> Dict[str, Any]:
    """
    Cluster challenges to a specific concept.

    Args:
        db: Database session
        concept_id: The concept being challenged
        concept_term: The concept term for context

    Returns:
        Dict with clustering results and created cluster IDs
    """
    # Get all pending challenges for this concept
    result = await db.execute(
        select(Challenge).where(
            Challenge.concept_id == concept_id,
            Challenge.status == ChallengeStatus.PENDING,
            Challenge.cluster_group_id.is_(None)  # Not already clustered
        )
    )
    challenges = result.scalars().all()

    if len(challenges) < 2:
        return {"status": "skipped", "reason": "Not enough challenges to cluster"}

    # Prepare challenge data for LLM
    challenge_data = []
    for ch in challenges:
        challenge_data.append({
            "id": ch.id,
            "project_id": ch.source_project_id,
            "project_name": ch.source_project_name or f"Project {ch.source_project_id}",
            "cluster_name": ch.source_cluster_name,
            "impact_type": ch.challenge_type.value if ch.challenge_type else "unknown",
            "summary": ch.impact_summary,
            "trend": ch.trend_description,
            "evidence": ch.key_evidence,
            "confidence": ch.confidence,
            "proposed_refinement": ch.proposed_refinement
        })

    # Call Claude for clustering analysis
    client = get_anthropic_client()

    user_prompt = f"""Analyze these {len(challenge_data)} challenges to the concept "{concept_term}":

{json.dumps(challenge_data, indent=2)}

Group similar challenges and provide recommendations. Remember to output valid JSON."""

    start_time = time.time()

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=CLUSTERING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    processing_time = time.time() - start_time

    # Parse response
    response_text = response.content[0].text

    # Extract JSON from response (handle markdown code blocks)
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()

    try:
        analysis = json.loads(response_text)
    except json.JSONDecodeError as e:
        return {
            "status": "error",
            "error": f"Failed to parse LLM response: {e}",
            "raw_response": response_text[:500]
        }

    # Create clusters in database
    created_clusters = []
    clustered_challenge_ids = []

    for cluster_data in analysis.get("clusters", []):
        challenge_ids = cluster_data.get("challenge_ids", [])
        if not challenge_ids:
            continue

        # Map recommendation to enum
        rec_str = cluster_data.get("recommendation", "human_review")
        rec_map = {
            "accept": RecommendedAction.ACCEPT,
            "reject": RecommendedAction.REJECT,
            "human_review": RecommendedAction.HUMAN_REVIEW,
            "merge": RecommendedAction.MERGE,
            "refine": RecommendedAction.REFINE
        }
        recommended_action = rec_map.get(rec_str, RecommendedAction.HUMAN_REVIEW)

        # Count unique projects
        member_challenges = [ch for ch in challenges if ch.id in challenge_ids]
        unique_projects = len(set(ch.source_project_id for ch in member_challenges))

        # Create cluster
        cluster = ChallengeCluster(
            cluster_type=ClusterType.CONCEPT_IMPACT,
            cluster_summary=cluster_data.get("summary"),
            cluster_recommendation=cluster_data.get("recommendation_rationale"),
            recommended_action=recommended_action,
            target_concept_id=concept_id,
            status=ClusterStatus.PENDING,
            member_count=len(challenge_ids),
            source_project_count=unique_projects
        )
        db.add(cluster)
        await db.flush()

        # Create cluster members
        for ch_id in challenge_ids:
            # Get similarity score based on consensus strength
            consensus = cluster_data.get("consensus_strength", "moderate")
            score_map = {"strong": 0.9, "moderate": 0.7, "weak": 0.5}
            similarity = score_map.get(consensus, 0.7)

            member = ChallengeClusterMember(
                cluster_id=cluster.id,
                challenge_id=ch_id,
                similarity_score=similarity
            )
            db.add(member)

            # Update challenge with cluster reference
            for ch in challenges:
                if ch.id == ch_id:
                    ch.cluster_group_id = cluster.id
                    clustered_challenge_ids.append(ch_id)
                    break

        created_clusters.append({
            "id": cluster.id,
            "summary": cluster_data.get("summary"),
            "member_count": len(challenge_ids),
            "recommendation": rec_str
        })

    await db.commit()

    return {
        "status": "success",
        "concept_term": concept_term,
        "total_challenges": len(challenges),
        "clustered_challenges": len(clustered_challenge_ids),
        "clusters_created": len(created_clusters),
        "clusters": created_clusters,
        "overall_assessment": analysis.get("overall_assessment"),
        "processing_time_seconds": round(processing_time, 2)
    }


async def cluster_dialectic_challenges(
    db: AsyncSession,
    dialectic_id: int,
    dialectic_name: str
) -> Dict[str, Any]:
    """
    Cluster challenges to a specific dialectic.
    Similar to concept clustering but for dialectical tensions.
    """
    result = await db.execute(
        select(Challenge).where(
            Challenge.dialectic_id == dialectic_id,
            Challenge.status == ChallengeStatus.PENDING,
            Challenge.cluster_group_id.is_(None)
        )
    )
    challenges = result.scalars().all()

    if len(challenges) < 2:
        return {"status": "skipped", "reason": "Not enough challenges to cluster"}

    challenge_data = []
    for ch in challenges:
        challenge_data.append({
            "id": ch.id,
            "project_id": ch.source_project_id,
            "project_name": ch.source_project_name or f"Project {ch.source_project_id}",
            "cluster_name": ch.source_cluster_name,
            "impact_type": ch.challenge_type.value if ch.challenge_type else "unknown",
            "summary": ch.impact_summary,
            "weight_toward_a": ch.weight_toward_a,
            "confidence": ch.confidence,
            "proposed_synthesis": ch.proposed_synthesis,
            "proposed_reframe": ch.proposed_reframe
        })

    client = get_anthropic_client()

    user_prompt = f"""Analyze these {len(challenge_data)} challenges to the dialectic "{dialectic_name}":

{json.dumps(challenge_data, indent=2)}

Group similar challenges and provide recommendations. Pay attention to which side of the dialectic each challenge supports (weight_toward_a: 0.0=fully B, 1.0=fully A).

Output valid JSON."""

    start_time = time.time()

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=CLUSTERING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    processing_time = time.time() - start_time

    response_text = response.content[0].text
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()

    try:
        analysis = json.loads(response_text)
    except json.JSONDecodeError as e:
        return {"status": "error", "error": f"Failed to parse: {e}"}

    created_clusters = []
    clustered_challenge_ids = []

    for cluster_data in analysis.get("clusters", []):
        challenge_ids = cluster_data.get("challenge_ids", [])
        if not challenge_ids:
            continue

        rec_str = cluster_data.get("recommendation", "human_review")
        rec_map = {
            "accept": RecommendedAction.ACCEPT,
            "reject": RecommendedAction.REJECT,
            "human_review": RecommendedAction.HUMAN_REVIEW
        }
        recommended_action = rec_map.get(rec_str, RecommendedAction.HUMAN_REVIEW)

        member_challenges = [ch for ch in challenges if ch.id in challenge_ids]
        unique_projects = len(set(ch.source_project_id for ch in member_challenges))

        cluster = ChallengeCluster(
            cluster_type=ClusterType.DIALECTIC_IMPACT,
            cluster_summary=cluster_data.get("summary"),
            cluster_recommendation=cluster_data.get("recommendation_rationale"),
            recommended_action=recommended_action,
            target_dialectic_id=dialectic_id,
            status=ClusterStatus.PENDING,
            member_count=len(challenge_ids),
            source_project_count=unique_projects
        )
        db.add(cluster)
        await db.flush()

        for ch_id in challenge_ids:
            consensus = cluster_data.get("consensus_strength", "moderate")
            score_map = {"strong": 0.9, "moderate": 0.7, "weak": 0.5}

            member = ChallengeClusterMember(
                cluster_id=cluster.id,
                challenge_id=ch_id,
                similarity_score=score_map.get(consensus, 0.7)
            )
            db.add(member)

            for ch in challenges:
                if ch.id == ch_id:
                    ch.cluster_group_id = cluster.id
                    clustered_challenge_ids.append(ch_id)
                    break

        created_clusters.append({
            "id": cluster.id,
            "summary": cluster_data.get("summary"),
            "member_count": len(challenge_ids),
            "recommendation": rec_str
        })

    await db.commit()

    return {
        "status": "success",
        "dialectic_name": dialectic_name,
        "total_challenges": len(challenges),
        "clustered_challenges": len(clustered_challenge_ids),
        "clusters_created": len(created_clusters),
        "clusters": created_clusters,
        "overall_assessment": analysis.get("overall_assessment"),
        "processing_time_seconds": round(processing_time, 2)
    }


async def cluster_emerging_concepts(db: AsyncSession) -> Dict[str, Any]:
    """
    Cluster similar emerging concepts from multiple projects.
    """
    result = await db.execute(
        select(EmergingConcept).where(
            EmergingConcept.status == EmergingStatus.PROPOSED,
            EmergingConcept.cluster_group_id.is_(None)
        )
    )
    emerging = result.scalars().all()

    if len(emerging) < 2:
        return {"status": "skipped", "reason": "Not enough emerging concepts to cluster"}

    ec_data = []
    for ec in emerging:
        ec_data.append({
            "id": ec.id,
            "project_id": ec.source_project_id,
            "project_name": ec.source_project_name or f"Project {ec.source_project_id}",
            "proposed_name": ec.proposed_name,
            "proposed_definition": ec.proposed_definition,
            "emergence_rationale": ec.emergence_rationale,
            "evidence_strength": ec.evidence_strength,
            "confidence": ec.confidence
        })

    client = get_anthropic_client()

    user_prompt = f"""Analyze these {len(ec_data)} proposed emerging concepts from different research projects:

{json.dumps(ec_data, indent=2)}

Identify which emerging concepts are essentially the same idea proposed independently by different projects. Group duplicates together and recommend whether the concept should be promoted to the theory base.

Output JSON with clusters of similar emerging concept IDs."""

    start_time = time.time()

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=4096,
        system=CLUSTERING_SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}]
    )

    processing_time = time.time() - start_time

    response_text = response.content[0].text
    if "```json" in response_text:
        json_start = response_text.find("```json") + 7
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()
    elif "```" in response_text:
        json_start = response_text.find("```") + 3
        json_end = response_text.find("```", json_start)
        response_text = response_text[json_start:json_end].strip()

    try:
        analysis = json.loads(response_text)
    except json.JSONDecodeError as e:
        return {"status": "error", "error": f"Failed to parse: {e}"}

    created_clusters = []
    clustered_ec_ids = []

    # Map challenge_ids to emerging concept IDs (LLM uses same field name)
    for cluster_data in analysis.get("clusters", []):
        ec_ids = cluster_data.get("challenge_ids", [])  # LLM might use this key
        if not ec_ids:
            ec_ids = cluster_data.get("emerging_concept_ids", [])  # Or this
        if not ec_ids:
            continue

        rec_str = cluster_data.get("recommendation", "human_review")
        rec_map = {
            "accept": RecommendedAction.ACCEPT,
            "reject": RecommendedAction.REJECT,
            "human_review": RecommendedAction.HUMAN_REVIEW,
            "merge": RecommendedAction.MERGE
        }
        recommended_action = rec_map.get(rec_str, RecommendedAction.HUMAN_REVIEW)

        member_ecs = [ec for ec in emerging if ec.id in ec_ids]
        unique_projects = len(set(ec.source_project_id for ec in member_ecs))

        cluster = ChallengeCluster(
            cluster_type=ClusterType.EMERGING_CONCEPT,
            cluster_summary=cluster_data.get("summary"),
            cluster_recommendation=cluster_data.get("recommendation_rationale"),
            recommended_action=recommended_action,
            status=ClusterStatus.PENDING,
            member_count=len(ec_ids),
            source_project_count=unique_projects
        )
        db.add(cluster)
        await db.flush()

        for ec_id in ec_ids:
            member = ChallengeClusterMember(
                cluster_id=cluster.id,
                emerging_concept_id=ec_id,
                similarity_score=0.8
            )
            db.add(member)

            for ec in emerging:
                if ec.id == ec_id:
                    ec.cluster_group_id = cluster.id
                    clustered_ec_ids.append(ec_id)
                    break

        created_clusters.append({
            "id": cluster.id,
            "summary": cluster_data.get("summary"),
            "member_count": len(ec_ids),
            "recommendation": rec_str
        })

    await db.commit()

    return {
        "status": "success",
        "total_emerging_concepts": len(emerging),
        "clustered": len(clustered_ec_ids),
        "clusters_created": len(created_clusters),
        "clusters": created_clusters,
        "processing_time_seconds": round(processing_time, 2)
    }


async def run_full_clustering(db: AsyncSession) -> Dict[str, Any]:
    """
    Run clustering on all pending challenges and emerging theory.
    """
    start_time = time.time()
    results = {
        "concept_clusters": [],
        "dialectic_clusters": [],
        "emerging_concept_clusters": None,
        "emerging_dialectic_clusters": None,
        "total_clusters_created": 0,
        "total_items_clustered": 0
    }

    # Get concepts with pending challenges
    concept_result = await db.execute(
        select(Concept.id, Concept.term, func.count(Challenge.id).label('count'))
        .join(Challenge, Challenge.concept_id == Concept.id)
        .where(Challenge.status == ChallengeStatus.PENDING)
        .group_by(Concept.id, Concept.term)
        .having(func.count(Challenge.id) >= 2)
    )

    for row in concept_result.fetchall():
        concept_id, concept_term, count = row
        result = await cluster_concept_challenges(db, concept_id, concept_term)
        results["concept_clusters"].append(result)
        if result.get("status") == "success":
            results["total_clusters_created"] += result.get("clusters_created", 0)
            results["total_items_clustered"] += result.get("clustered_challenges", 0)

    # Get dialectics with pending challenges
    dialectic_result = await db.execute(
        select(Dialectic.id, Dialectic.name, func.count(Challenge.id).label('count'))
        .join(Challenge, Challenge.dialectic_id == Dialectic.id)
        .where(Challenge.status == ChallengeStatus.PENDING)
        .group_by(Dialectic.id, Dialectic.name)
        .having(func.count(Challenge.id) >= 2)
    )

    for row in dialectic_result.fetchall():
        dialectic_id, dialectic_name, count = row
        result = await cluster_dialectic_challenges(db, dialectic_id, dialectic_name)
        results["dialectic_clusters"].append(result)
        if result.get("status") == "success":
            results["total_clusters_created"] += result.get("clusters_created", 0)
            results["total_items_clustered"] += result.get("clustered_challenges", 0)

    # Cluster emerging concepts
    ec_result = await cluster_emerging_concepts(db)
    results["emerging_concept_clusters"] = ec_result
    if ec_result.get("status") == "success":
        results["total_clusters_created"] += ec_result.get("clusters_created", 0)
        results["total_items_clustered"] += ec_result.get("clustered", 0)

    results["processing_time_seconds"] = round(time.time() - start_time, 2)

    return results
