"""
Demand-Side Semantic Scoring Engine
====================================
A cutting-edge NLP system that quantifies geopolitical and economic risk
by decomposing news events into semantic primitives, generating ordered
probability sets from existence and sentiment relations, and calibrating
distributions using known anchor probabilities.

Core Innovation: Converts qualitative news narratives into quantitative
probability distributions using ordered set theory and semantic relations.

Author: Jefferson Richards
Based on original research (2018) - modernized with transformer architectures.
"""

import numpy as np
from dataclasses import dataclass, field
from typing import Optional
import json
import re
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")


# ============================================================================
# CONFIGURATION
# ============================================================================

SPACY_MODEL = "en_core_web_sm"
TRANSFORMER_MODEL = "all-MiniLM-L6-v2"


# ============================================================================
# DATA STRUCTURES
# ============================================================================

@dataclass
class PhenDecomposition:
    """Phenomenological decomposition of a news event."""
    timestamp: datetime
    subjects: list[str]
    concepts: list[str]
    primes: list[str]
    source_text: str
    source_url: str = ""


@dataclass
class BlueConcept:
    """A 'blue word' — a concept retained after business rule reduction."""
    term: str
    antonym: str
    frequency: int = 0
    proximity_to_subject: float = 0.0
    embedding: Optional[np.ndarray] = field(default=None, repr=False)


@dataclass
class OrderedRelationSet:
    """An ordered set representing either existence or sentiment relation."""
    subject: str
    relation_type: str  # 'existence' or 'sentiment'
    concepts: list[str]
    antonyms: list[str]
    probabilities: list[float]
    antonym_probabilities: list[float]
    anchor_probability: Optional[float] = None
    anchor_concept: Optional[str] = None

    @property
    def combined_set(self) -> dict[str, float]:
        """Combine concepts and antonyms into full ordered distribution.

        When a term appears as both a concept (with its own calibrated
        probability) AND as the antonym of another concept, the concept's
        own probability takes precedence — it's the directly calibrated value.
        """
        concept_set = set(self.concepts)
        combined = {}
        for c, p in zip(self.concepts, self.probabilities):
            combined[c] = p
        for a, p in zip(self.antonyms, self.antonym_probabilities):
            # Only add the antonym if it isn't already present as a concept
            # with its own directly calibrated probability
            if a not in concept_set:
                combined[a] = p
        return dict(sorted(combined.items(), key=lambda x: x[1]))


@dataclass
class SemanticScoreResult:
    """Complete scoring result for a news event."""
    event_text: str
    timestamp: datetime
    decomposition: PhenDecomposition
    existence_relations: list[OrderedRelationSet]
    sentiment_relations: list[OrderedRelationSet]
    aggregate_risk_score: float
    interpretation: str


# ============================================================================
# ANTONYM KNOWLEDGE BASE
# ============================================================================

# Curated antonym pairs for economic/geopolitical domain
DOMAIN_ANTONYMS = {
    "loss": "gain",
    "gain": "loss",
    "risk": "impossibility",
    "impossibility": "risk",
    "tariff": "rebate",
    "rebate": "tariff",
    "inflation": "deflation",
    "deflation": "inflation",
    "recession": "expansion",
    "expansion": "recession",
    "default": "solvency",
    "solvency": "default",
    "sanctions": "trade",
    "trade": "sanctions",
    "volatility": "stability",
    "stability": "volatility",
    "debt": "surplus",
    "surplus": "debt",
    "decline": "growth",
    "growth": "decline",
    "war": "peace",
    "peace": "war",
    "scarcity": "abundance",
    "abundance": "scarcity",
    "uncertainty": "certainty",
    "certainty": "uncertainty",
    "devaluation": "appreciation",
    "appreciation": "devaluation",
    "crisis": "recovery",
    "recovery": "crisis",
    "collapse": "resilience",
    "resilience": "collapse",
    "contagion": "containment",
    "containment": "contagion",
    "disruption": "continuity",
    "continuity": "disruption",
    "fragmentation": "integration",
    "integration": "fragmentation",
}


# Blue words: domain-critical concepts that anchor existence relations
BLUE_WORDS = set(DOMAIN_ANTONYMS.keys())


# ============================================================================
# CORE ENGINE
# ============================================================================

class DemandSideSemanticScorer:
    """
    Implements the Demand-Side Semantic Scoring methodology.

    The key insight: qualitative narratives can be converted to quantitative
    probability distributions by:
    1. Decomposing events into subjects, concepts, and primes
    2. Filtering concepts through 'blue word' domain vocabulary
    3. Generating ordered sets based on existence (frequency) and
       sentiment (proximity) relations
    4. Assigning linear probabilities to the ordering
    5. Calibrating with known anchor probabilities via Bayesian update

    This bridges the gap between positive statements (what IS) and
    normative statements (what OUGHT to be) — the missing half of
    traditional sentiment analysis.
    """

    def __init__(self):
        self._nlp = None
        self._sentence_model = None

    @property
    def nlp(self):
        """Lazy-load spaCy model."""
        if self._nlp is None:
            try:
                import spacy
                self._nlp = spacy.load(SPACY_MODEL)
            except (ImportError, OSError):
                self._nlp = None
        return self._nlp

    @property
    def sentence_model(self):
        """Lazy-load sentence transformer for semantic similarity."""
        if self._sentence_model is None:
            try:
                from sentence_transformers import SentenceTransformer
                self._sentence_model = SentenceTransformer(TRANSFORMER_MODEL)
            except ImportError:
                self._sentence_model = None
        return self._sentence_model

    def decompose_event(self, text: str, timestamp: str = None,
                        url: str = "") -> PhenDecomposition:
        """
        Phenomenological decomposition: break event into semantic primitives.

        Uses NER for subjects, noun chunks + blue word filtering for concepts,
        and function words for primes.
        """
        if timestamp is None:
            timestamp = datetime.now().isoformat()

        ts = datetime.fromisoformat(timestamp) if isinstance(timestamp, str) else timestamp

        subjects = []
        concepts = []
        primes = []

        if self.nlp:
            doc = self.nlp(text)

            # Extract subjects via named entities
            for ent in doc.ents:
                if ent.label_ in ("PERSON", "ORG", "GPE", "NORP", "EVENT"):
                    subjects.append(ent.text)

            # Extract concepts via noun chunks and verb phrases
            for chunk in doc.noun_chunks:
                chunk_lower = chunk.text.lower()
                if any(bw in chunk_lower for bw in BLUE_WORDS):
                    concepts.append(chunk.text.lower())
                elif chunk.root.dep_ in ("nsubj", "dobj", "pobj"):
                    concepts.append(chunk.text.lower())

            # Primes are function words and auxiliaries
            for token in doc:
                if token.pos_ in ("AUX", "ADP", "SCONJ", "CCONJ", "PART"):
                    primes.append(token.text.lower())
        else:
            # Fallback: regex-based extraction
            subjects = re.findall(r'[A-Z][a-z]+ [A-Z][a-z]+|[A-Z]{2,}', text)
            words = text.lower().split()
            concepts = [w for w in words if w in BLUE_WORDS]
            primes = [w for w in words if len(w) <= 3]

        # Deduplicate while preserving order
        subjects = list(dict.fromkeys(subjects))
        concepts = list(dict.fromkeys(concepts))

        return PhenDecomposition(
            timestamp=ts,
            subjects=subjects,
            concepts=concepts,
            primes=primes,
            source_text=text,
            source_url=url
        )

    def extract_blue_concepts(self, text: str,
                              concepts: list[str]) -> list[BlueConcept]:
        """
        Identify 'blue words' — domain-critical concepts retained after
        business rule reduction. These anchor the existence relation.
        """
        text_lower = text.lower()
        blue_concepts = []

        for concept in concepts:
            # Check if any blue word appears in this concept
            for bw in BLUE_WORDS:
                if bw in concept:
                    antonym = DOMAIN_ANTONYMS.get(bw, f"not_{bw}")
                    frequency = text_lower.count(bw)
                    blue_concepts.append(BlueConcept(
                        term=bw,
                        antonym=antonym,
                        frequency=frequency
                    ))
                    break

        # Also scan full text for blue words not in extracted concepts
        for bw in BLUE_WORDS:
            if bw in text_lower:
                already_found = any(bc.term == bw for bc in blue_concepts)
                if not already_found:
                    blue_concepts.append(BlueConcept(
                        term=bw,
                        antonym=DOMAIN_ANTONYMS.get(bw, f"not_{bw}"),
                        frequency=text_lower.count(bw)
                    ))

        # Deduplicate
        seen = set()
        unique = []
        for bc in blue_concepts:
            if bc.term not in seen:
                seen.add(bc.term)
                unique.append(bc)

        return unique

    def compute_proximity(self, text: str, subject: str,
                          concept: str) -> float:
        """
        Compute semantic proximity between a subject and concept.

        Uses sentence-transformer cosine similarity when available,
        falls back to token distance in text.
        """
        if self.sentence_model:
            embeddings = self.sentence_model.encode([subject, concept])
            cos_sim = np.dot(embeddings[0], embeddings[1]) / (
                np.linalg.norm(embeddings[0]) * np.linalg.norm(embeddings[1])
            )
            return float(cos_sim)

        # Fallback: normalized word distance in text
        text_lower = text.lower()
        subj_pos = text_lower.find(subject.lower())
        conc_pos = text_lower.find(concept.lower())

        if subj_pos == -1 or conc_pos == -1:
            return 0.0

        distance = abs(subj_pos - conc_pos)
        max_dist = len(text_lower)
        return 1.0 - (distance / max_dist) if max_dist > 0 else 0.0

    def generate_existence_ordering(self, blue_concepts: list[BlueConcept],
                                    subject: str) -> list[str]:
        """
        Order concepts by frequency for existence relation.
        Lower frequency = less probable existence = earlier in ordered set.
        """
        sorted_concepts = sorted(blue_concepts, key=lambda bc: bc.frequency)
        return [bc.term for bc in sorted_concepts]

    def generate_sentiment_ordering(self, text: str,
                                    blue_concepts: list[BlueConcept],
                                    subject: str) -> list[str]:
        """
        Order concepts by proximity to subject for sentiment relation.
        Greater distance = less probable sentiment = earlier in ordered set.
        """
        proximities = []
        for bc in blue_concepts:
            prox = self.compute_proximity(text, subject, bc.term)
            proximities.append((bc.term, prox))

        # Sort by proximity ascending (farthest = least probable)
        sorted_by_prox = sorted(proximities, key=lambda x: x[1])
        return [term for term, _ in sorted_by_prox]

    def assign_linear_probabilities(self, n_concepts: int) -> list[float]:
        """
        Assign linearly distributed probabilities to an ordered set.
        p(i) = i / (2 * n) for i in 1..n
        This gives the 'uninformed prior' distribution.
        """
        return [(i + 1) / (2 * n_concepts) for i in range(n_concepts)]

    def calibrate_with_anchor(self, ordered_concepts: list[str],
                              probabilities: list[float],
                              anchor_concept: str,
                              anchor_probability: float) -> list[float]:
        """
        Anchor-ripple calibration: given a known probability for one
        concept in the ordered set, redistribute ALL other probabilities
        so that the ordering is preserved and the spread fans out
        naturally from the anchor point.

        The key insight from the original research: concepts BELOW the
        anchor in the ordering get probabilities linearly distributed
        in [0, anchor_p], and concepts ABOVE get probabilities linearly
        distributed in [anchor_p, 1]. The anchor acts as a fulcrum —
        one known value reshapes the entire distribution.

        This produces a visible "ripple effect" where each concept's
        probability is uniquely determined by its position relative to
        the anchor.
        """
        if anchor_concept not in ordered_concepts:
            return probabilities

        anchor_idx = ordered_concepts.index(anchor_concept)
        n = len(ordered_concepts)
        calibrated = [0.0] * n

        # Fix the anchor probability
        calibrated[anchor_idx] = anchor_probability

        # Concepts BELOW anchor (indices 0..anchor_idx-1):
        # Linearly distribute in (0, anchor_p)
        # Concept at position 0 gets the lowest probability,
        # concept at position anchor_idx-1 gets just below anchor_p
        n_below = anchor_idx
        if n_below > 0:
            for i in range(n_below):
                # Linear interpolation: rank (i+1) out of (n_below+1)
                # slots in the interval (0, anchor_p)
                calibrated[i] = anchor_probability * (i + 1) / (n_below + 1)

        # Concepts ABOVE anchor (indices anchor_idx+1..n-1):
        # Linearly distribute in (anchor_p, 1)
        # Concept just above anchor gets just above anchor_p,
        # concept at position n-1 gets close to 1.0
        n_above = n - anchor_idx - 1
        if n_above > 0:
            for j in range(n_above):
                idx = anchor_idx + 1 + j
                # Linear interpolation: rank (j+1) out of (n_above+1)
                # slots in the interval (anchor_p, 1)
                calibrated[idx] = anchor_probability + \
                    (1.0 - anchor_probability) * (j + 1) / (n_above + 1)

        return calibrated

    def build_relation_set(self, subject: str, concepts: list[str],
                           relation_type: str,
                           anchor_concept: str = None,
                           anchor_probability: float = None
                           ) -> OrderedRelationSet:
        """
        Build a complete ordered relation set with antonyms and probabilities.
        """
        n = len(concepts)
        if n == 0:
            return OrderedRelationSet(
                subject=subject, relation_type=relation_type,
                concepts=[], antonyms=[], probabilities=[],
                antonym_probabilities=[]
            )

        # Get antonyms
        antonyms = [DOMAIN_ANTONYMS.get(c, f"not_{c}") for c in concepts]

        # Assign base probabilities
        probs = self.assign_linear_probabilities(n)

        # Calibrate if anchor is provided
        if anchor_concept and anchor_probability is not None:
            probs = self.calibrate_with_anchor(
                concepts, probs, anchor_concept, anchor_probability
            )

        # Antonym probabilities are complements
        antonym_probs = [1.0 - p for p in probs]

        return OrderedRelationSet(
            subject=subject,
            relation_type=relation_type,
            concepts=concepts,
            antonyms=antonyms,
            probabilities=probs,
            antonym_probabilities=antonym_probs,
            anchor_probability=anchor_probability,
            anchor_concept=anchor_concept
        )

    def compute_aggregate_risk(
            self, relations: list[OrderedRelationSet]) -> float:
        """
        Compute aggregate risk score from all relation sets.

        Risk is measured as the weighted probability mass concentrated
        in negative-valence concepts (those whose antonyms are positive).
        Score ranges from 0 (no risk) to 1 (maximum risk).
        """
        if not relations:
            return 0.5

        negative_concepts = {
            "loss", "risk", "tariff", "inflation", "recession", "default",
            "sanctions", "volatility", "debt", "decline", "war", "scarcity",
            "uncertainty", "devaluation", "crisis", "collapse", "contagion",
            "disruption", "fragmentation"
        }

        total_weight = 0.0
        risk_weight = 0.0

        for rel in relations:
            for concept, prob in zip(rel.concepts, rel.probabilities):
                total_weight += prob
                if concept in negative_concepts:
                    risk_weight += prob

        return risk_weight / total_weight if total_weight > 0 else 0.5

    def generate_interpretation(self, subject: str,
                                relation: OrderedRelationSet) -> str:
        """Generate natural language interpretation of ordered set."""
        combined = relation.combined_set
        sorted_items = sorted(combined.items(), key=lambda x: x[1])

        if not sorted_items:
            return "Insufficient data for interpretation."

        least_probable = sorted_items[0][0]
        most_probable = sorted_items[-1][0]
        relation_verb = "expresses to exist" if relation.relation_type == \
            "existence" else "feels about"

        interp = (
            f"Running a simulation of events that {subject} "
            f"{relation_verb}: the least likely outcome is '{least_probable}' "
            f"(p={sorted_items[0][1]:.3f}) and the most likely outcome is "
            f"'{most_probable}' (p={sorted_items[-1][1]:.3f})."
        )

        if relation.anchor_concept:
            interp += (
                f" [Calibrated with known p({relation.anchor_concept})"
                f"={relation.anchor_probability:.3f}]"
            )

        return interp

    def score_event(self, text: str, timestamp: str = None,
                    url: str = "",
                    anchors: dict[str, float] = None
                    ) -> SemanticScoreResult:
        """
        Full pipeline: decompose event, extract blue concepts, build
        ordered sets, calibrate, and produce final score.

        Parameters
        ----------
        text : str
            Raw news article text or headline
        timestamp : str
            ISO timestamp of the event
        url : str
            Source URL
        anchors : dict
            Known probabilities for specific concepts,
            e.g. {"tariff": 0.65}
        """
        if anchors is None:
            anchors = {}

        # Step 1: Phenomenological decomposition
        decomp = self.decompose_event(text, timestamp, url)

        # Step 2: Extract blue concepts
        blue_concepts = self.extract_blue_concepts(text, decomp.concepts)

        if not blue_concepts:
            return SemanticScoreResult(
                event_text=text,
                timestamp=decomp.timestamp,
                decomposition=decomp,
                existence_relations=[],
                sentiment_relations=[],
                aggregate_risk_score=0.5,
                interpretation="No domain-critical concepts detected."
            )

        existence_relations = []
        sentiment_relations = []

        # Step 3-5: For each subject, build existence and sentiment relations
        for subject in decomp.subjects:
            # Existence: ordered by frequency
            exist_order = self.generate_existence_ordering(
                blue_concepts, subject
            )

            # Sentiment: ordered by proximity
            sent_order = self.generate_sentiment_ordering(
                text, blue_concepts, subject
            )

            # Determine anchor for this ordering
            anchor_concept = None
            anchor_prob = None
            for concept in exist_order:
                if concept in anchors:
                    anchor_concept = concept
                    anchor_prob = anchors[concept]
                    break

            # Build relation sets
            exist_rel = self.build_relation_set(
                subject, exist_order, "existence",
                anchor_concept, anchor_prob
            )
            sent_rel = self.build_relation_set(
                subject, sent_order, "sentiment",
                anchor_concept, anchor_prob
            )

            existence_relations.append(exist_rel)
            sentiment_relations.append(sent_rel)

        # Step 6: Aggregate risk score
        all_relations = existence_relations + sentiment_relations
        risk_score = self.compute_aggregate_risk(all_relations)

        # Step 7: Generate interpretation
        interpretations = []
        for rel in existence_relations:
            interpretations.append(
                self.generate_interpretation(rel.subject, rel)
            )
        for rel in sentiment_relations:
            interpretations.append(
                self.generate_interpretation(rel.subject, rel)
            )

        return SemanticScoreResult(
            event_text=text,
            timestamp=decomp.timestamp,
            decomposition=decomp,
            existence_relations=existence_relations,
            sentiment_relations=sentiment_relations,
            aggregate_risk_score=risk_score,
            interpretation="\n\n".join(interpretations)
        )


# ============================================================================
# VISUALIZATION
# ============================================================================

def generate_visualization(result: SemanticScoreResult,
                           output_path: str) -> str:
    """
    Generate a publication-quality PNG visualization of the scoring results.

    Shows:
    - Probability distributions (before/after calibration)
    - Combined ordered sets
    - Aggregate risk gauge
    """
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch, Arc
    from matplotlib.colors import LinearSegmentedColormap
    import matplotlib.patheffects as pe

    # Style setup
    plt.rcParams.update({
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica", "Arial", "DejaVu Sans"],
        "font.size": 10,
        "axes.spines.top": False,
        "axes.spines.right": False,
    })

    fig = plt.figure(figsize=(16, 10), facecolor="#0a0a1a")

    # Custom colormap: risk gradient
    risk_cmap = LinearSegmentedColormap.from_list(
        "risk", ["#00d4aa", "#ffd700", "#ff4444"]
    )

    # Title
    fig.text(0.5, 0.96, "DEMAND-SIDE SEMANTIC SCORE",
             ha="center", va="top", fontsize=20, fontweight="bold",
             color="white",
             path_effects=[pe.withStroke(linewidth=2, foreground="#333")])
    fig.text(0.5, 0.925,
             "Quantifying Geopolitical Risk via Ordered Set Theory",
             ha="center", va="top", fontsize=11, color="#aaaaaa")

    # --- Panel 1: Anchor Ripple Effect (top — full width) ---
    ax1 = fig.add_axes([0.05, 0.52, 0.9, 0.35])
    ax1.set_facecolor("#111122")

    if result.existence_relations:
        rel = result.existence_relations[0]

        # Use concepts + antonyms together in the combined ordered set
        combined = rel.combined_set
        labels = list(combined.keys())
        values = list(combined.values())
        n_items = len(labels)

        # Determine which items are the anchor concept/antonym
        anchor_name = rel.anchor_concept
        anchor_p = rel.anchor_probability

        # Color bars: anchor in gold, concepts below in teal gradient,
        # concepts above in red gradient
        colors = []
        for i, (lbl, val) in enumerate(zip(labels, values)):
            if lbl == anchor_name:
                colors.append("#ffd700")  # gold for anchor
            elif val < (anchor_p if anchor_p else 0.5):
                # Below anchor — teal/green gradient
                t = val / (anchor_p if anchor_p else 0.5)
                colors.append(risk_cmap(0.15 + 0.2 * t))
            else:
                # Above anchor — orange/red gradient
                t = (val - (anchor_p if anchor_p else 0.5)) / \
                    (1.0 - (anchor_p if anchor_p else 0.5))
                colors.append(risk_cmap(0.5 + 0.5 * t))

        bars = ax1.barh(range(n_items), values, color=colors,
                        edgecolor="#222", linewidth=0.5, height=0.7)
        ax1.set_yticks(range(n_items))
        ax1.set_yticklabels(labels, fontsize=8, color="white")
        ax1.set_xlim(0, 1.15)
        ax1.set_xlabel("Probability", color="#aaa", fontsize=9)
        ax1.tick_params(colors="#aaa")

        title_str = (f"ANCHOR RIPPLE: p({anchor_name}) = "
                     f"{anchor_p:.2f} → reshapes entire distribution"
                     if anchor_name else
                     f"Existence Relation: {rel.subject}")
        ax1.set_title(title_str, color="white", fontsize=12,
                      fontweight="bold", pad=10)

        # Add probability labels on bars
        for bar, val, lbl in zip(bars, values, labels):
            weight = "bold" if lbl == anchor_name else "normal"
            color = "#ffd700" if lbl == anchor_name else "#ddd"
            ax1.text(bar.get_width() + 0.01,
                     bar.get_y() + bar.get_height() / 2,
                     f"{val:.3f}", va="center", fontsize=7.5,
                     color=color, fontweight=weight)

        # Draw anchor line
        if anchor_p:
            ax1.axvline(x=anchor_p, color="#ffd700",
                        linestyle="--", linewidth=2, alpha=0.9)
            # Find anchor y position
            if anchor_name in labels:
                anchor_y = labels.index(anchor_name)
                ax1.annotate(
                    f"ANCHOR\np({anchor_name})={anchor_p:.2f}",
                    xy=(anchor_p, anchor_y),
                    xytext=(min(anchor_p + 0.15, 0.92), anchor_y + 2.5),
                    fontsize=9, color="#ffd700", fontweight="bold",
                    ha="center",
                    arrowprops=dict(arrowstyle="->", color="#ffd700",
                                    lw=1.5))
    else:
        ax1.text(0.5, 0.5, "No existence relations", ha="center",
                 va="center", color="#666", fontsize=12)

    ax1.spines["bottom"].set_color("#333")
    ax1.spines["left"].set_color("#333")

    # --- Panel 3: Risk Gauge (bottom left) ---
    ax3 = fig.add_axes([0.05, 0.08, 0.35, 0.35])
    ax3.set_facecolor("#0a0a1a")
    ax3.set_xlim(-1.5, 1.5)
    ax3.set_ylim(-0.5, 1.5)
    ax3.set_aspect("equal")
    ax3.axis("off")

    # Draw gauge arc
    theta_range = np.linspace(180, 0, 100)
    for i in range(len(theta_range) - 1):
        t = i / (len(theta_range) - 1)
        color = risk_cmap(t)
        arc = Arc((0, 0), 2.4, 2.4,
                  angle=0, theta1=theta_range[i+1], theta2=theta_range[i],
                  color=color, linewidth=8)
        ax3.add_patch(arc)

    # Needle
    risk = result.aggregate_risk_score
    needle_angle = np.radians(180 - risk * 180)
    needle_x = 1.0 * np.cos(needle_angle)
    needle_y = 1.0 * np.sin(needle_angle)
    ax3.plot([0, needle_x], [0, needle_y], color="white", linewidth=2.5,
             solid_capstyle="round")
    ax3.plot(0, 0, "o", color="white", markersize=8)

    # Labels
    ax3.text(0, -0.35, f"AGGREGATE RISK: {risk:.2f}",
             ha="center", fontsize=14, fontweight="bold",
             color=risk_cmap(risk))
    ax3.text(-1.3, -0.1, "LOW", ha="center", fontsize=9, color="#00d4aa")
    ax3.text(1.3, -0.1, "HIGH", ha="center", fontsize=9, color="#ff4444")
    ax3.text(0, 1.35, "RISK GAUGE", ha="center", fontsize=11,
             fontweight="bold", color="white")

    # --- Panel 4: Interpretation & Metadata (bottom right) ---
    import textwrap

    ax4 = fig.add_axes([0.45, 0.08, 0.5, 0.35])
    ax4.set_facecolor("#111122")
    ax4.axis("off")

    # Add interpretation box
    box = FancyBboxPatch((0.02, 0.02), 0.96, 0.96,
                         boxstyle="round,pad=0.02",
                         facecolor="#1a1a2e", edgecolor="#333",
                         linewidth=1)
    ax4.add_patch(box)

    # Wrap width for text content (characters per line)
    wrap_width = 72

    # Event text (wrapped)
    event_display = result.event_text[:180] + "..." \
        if len(result.event_text) > 180 else result.event_text
    event_wrapped = textwrap.fill(event_display, width=wrap_width)

    ax4.text(0.05, 0.95, "EVENT", fontsize=9, fontweight="bold",
             color="#ffd700", transform=ax4.transAxes,
             verticalalignment="top")
    ax4.text(0.05, 0.88, event_wrapped, fontsize=7.5, color="#ccc",
             transform=ax4.transAxes,
             verticalalignment="top", family="monospace")

    ax4.text(0.05, 0.68, "SUBJECTS", fontsize=9, fontweight="bold",
             color="#00d4aa", transform=ax4.transAxes,
             verticalalignment="top")
    subjects_str = ", ".join(result.decomposition.subjects[:5])
    ax4.text(0.05, 0.62, subjects_str, fontsize=9, color="#ccc",
             transform=ax4.transAxes, verticalalignment="top")

    ax4.text(0.05, 0.52, "BLUE CONCEPTS", fontsize=9, fontweight="bold",
             color="#4da6ff", transform=ax4.transAxes,
             verticalalignment="top")
    if result.existence_relations:
        concepts_list = result.existence_relations[0].concepts[:8]
        concepts_str = " → ".join(concepts_list)
        if len(result.existence_relations[0].concepts) > 8:
            concepts_str += " → ..."
    else:
        concepts_str = "None detected"
    concepts_wrapped = textwrap.fill(concepts_str, width=wrap_width)
    ax4.text(0.05, 0.46, concepts_wrapped, fontsize=8, color="#ccc",
             transform=ax4.transAxes, verticalalignment="top",
             family="monospace")

    ax4.text(0.05, 0.30, "INTERPRETATION", fontsize=9, fontweight="bold",
             color="#ff9944", transform=ax4.transAxes,
             verticalalignment="top")
    # Take first interpretation only and wrap it properly
    first_interp = result.interpretation.split("\n\n")[0] \
        if result.interpretation else "Insufficient data."
    if len(first_interp) > 250:
        first_interp = first_interp[:247] + "..."
    interp_wrapped = textwrap.fill(first_interp, width=wrap_width)
    ax4.text(0.05, 0.24, interp_wrapped, fontsize=7.5, color="#aaa",
             transform=ax4.transAxes, verticalalignment="top",
             family="monospace")

    # Footer
    fig.text(0.5, 0.02,
             f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')} | "
             f"Model: Demand-Side Semantic Scoring v2.0 | "
             f"© Richards Research",
             ha="center", fontsize=8, color="#555")

    plt.savefig(output_path, dpi=200, bbox_inches="tight",
                facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close()

    return output_path


# ============================================================================
# DEMONSTRATION
# ============================================================================

def run_demo():
    """
    Demonstrate the scoring engine on a modern geopolitical event,
    showing both uncalibrated and calibrated distributions.
    """
    scorer = DemandSideSemanticScorer()

    # Modern event: a realistic 2026 geopolitical scenario
    event_text = (
        "The Federal Reserve warned that escalating semiconductor sanctions "
        "against China pose systemic risk to global supply chains. "
        "Treasury Secretary noted the trade war's potential for economic "
        "contagion, with volatility in emerging markets signaling possible "
        "recession if disruption continues. Analysts estimate a 72% "
        "probability of further tariff escalation, raising uncertainty "
        "about growth prospects for the US economy."
    )

    print("=" * 70)
    print("DEMAND-SIDE SEMANTIC SCORING ENGINE v2.0")
    print("Bridging Positive and Normative Analysis in NLP")
    print("=" * 70)

    # Score without anchors (uninformed prior)
    print("\n[1] SCORING WITH UNINFORMED PRIOR (Linear Distribution)")
    print("-" * 50)
    result_linear = scorer.score_event(
        text=event_text,
        timestamp="2026-07-09T14:30:00",
        url="https://reuters.com/example"
    )

    print(f"\nSubjects: {result_linear.decomposition.subjects}")
    print(f"Blue Concepts Detected: "
          f"{[r.concepts for r in result_linear.existence_relations]}")
    print(f"Aggregate Risk Score: {result_linear.aggregate_risk_score:.4f}")
    print(f"\nInterpretation:\n{result_linear.interpretation}")

    # Score WITH anchor probabilities (calibrated)
    print("\n\n[2] SCORING WITH KNOWN ANCHORS (Bayesian Calibration)")
    print("-" * 50)
    anchors = {"tariff": 0.72, "sanctions": 0.80}
    print(f"Known anchors: {anchors}")

    result_calibrated = scorer.score_event(
        text=event_text,
        timestamp="2026-07-09T14:30:00",
        url="https://reuters.com/example",
        anchors=anchors
    )

    print(f"\nAggregate Risk Score: "
          f"{result_calibrated.aggregate_risk_score:.4f}")
    print(f"\nInterpretation:\n{result_calibrated.interpretation}")

    # Show combined ordered sets
    if result_calibrated.existence_relations:
        print("\n\n[3] COMBINED ORDERED SETS (Calibrated)")
        print("-" * 50)
        for rel in result_calibrated.existence_relations:
            print(f"\n  {rel.subject} — {rel.relation_type.upper()}:")
            combined = rel.combined_set
            for concept, prob in sorted(combined.items(), key=lambda x: x[1]):
                marker = "●" if concept in rel.concepts else "○"
                print(f"    {marker} {concept:20s} p = {prob:.4f}")

    # Generate visualization
    print("\n\n[4] GENERATING VISUALIZATION")
    print("-" * 50)
    output_dir = "/Users/jefferson/000_coderepo/riskrunners/models/" \
                 "demandSideSemanticScore"
    viz_path = f"{output_dir}/demand_side_semantic_score_output.png"

    generate_visualization(result_calibrated, viz_path)
    print(f"Visualization saved to: {viz_path}")

    # Output structured data
    print("\n\n[5] STRUCTURED OUTPUT (JSON)")
    print("-" * 50)
    output_data = {
        "timestamp": result_calibrated.timestamp.isoformat(),
        "aggregate_risk_score": result_calibrated.aggregate_risk_score,
        "subjects": result_calibrated.decomposition.subjects,
        "anchors_used": anchors,
        "existence_relations": [
            {
                "subject": r.subject,
                "ordered_set": r.combined_set
            }
            for r in result_calibrated.existence_relations
        ],
        "sentiment_relations": [
            {
                "subject": r.subject,
                "ordered_set": r.combined_set
            }
            for r in result_calibrated.sentiment_relations
        ],
    }
    print(json.dumps(output_data, indent=2, default=str))

    return result_calibrated, viz_path


if __name__ == "__main__":
    result, viz_path = run_demo()
