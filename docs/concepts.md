# Key Concepts in Tendon Fate Mapping

A reference guide for new students. Terms are explained from the ground up, with links to relevant papers in [`docs/papers/papers.md`](papers/papers.md).

---

## Contents

1. [Cell Types](#1-cell-types)
   - [Fibroadipogenic Progenitors (FAPs)](#fibroadipogenic-progenitors-faps)
   - [Mesenchymal Progenitors (MPs)](#mesenchymal-progenitors-mps)
   - [Mesenchymal Stromal Cells (MSCs)](#mesenchymal-stromal-cells-mscs)
   - [Fibroblasts](#fibroblasts)
   - [Tendon Stem/Progenitor Cells (TSPCs)](#tendon-stemprogenitor-cells-tspcs)
   - [Tenocytes](#tenocytes)
2. [Biological Processes](#2-biological-processes)
   - [Tendon Regeneration](#tendon-regeneration)
   - [Musculoskeletal Regeneration](#musculoskeletal-regeneration)
3. [Experimental Models](#3-experimental-models)
   - [Tendon Injury Models](#tendon-injury-models)
   - [Bone Fracture / Skeletal Injury Models](#bone-fracture--skeletal-injury-models)
4. [Laboratory Methods](#4-laboratory-methods)
   - [Lineage Tracing (Cre-lox and CreERT2)](#lineage-tracing-cre-lox-and-creert2)
   - [Immunofluorescence (IF)](#immunofluorescence-if)
   - [Bulk RNA-seq](#bulk-rna-seq)
   - [Single-Cell RNA-seq and ATAC-seq](#single-cell-rna-seq-and-atac-seq)
   - [Spatial Transcriptomics (Visium and Xenium)](#spatial-transcriptomics-visium-and-xenium)
5. [Translational Tools](#5-translational-tools)
   - [Biomaterial Scaffolds and Microphysiological Structures](#biomaterial-scaffolds-and-microphysiological-structures)

---

## 1. Cell Types

### Fibroadipogenic Progenitors (FAPs)

**What they are:** FAPs are a population of stromal (connective tissue) stem cells that live in the spaces between muscle fibers, tendons, and other soft tissues. The name comes from their two main differentiation potentials: they can become **fibro**blasts (cells that make connective tissue matrix) or **adipo**cytes (fat cells) depending on the signals they receive. They are identified by the surface markers PDGFRα+ and Sca-1+ (also written Ly6a+).

**Why they matter:** Under normal conditions FAPs are largely quiescent (dormant), but after tissue injury they activate rapidly — clearing debris, secreting growth factors, and organizing the regenerative environment. If FAP activity is not properly controlled, they can produce excess scar tissue or fat deposits instead of functional tissue (fibrofatty infiltration). FAPs in skeletal muscle have been subdivided into two major groups:

- **FAP1** (Dpt+, Col15a1+): Enriched for extracellular matrix (ECM) genes like Col4a1, Col6, Bgn. These cells are structural architects of the regenerating tissue.
- **FAP2** (Dpt+, Pi16+): Enriched for trophic/signaling genes like Sfrp4, Wnt2, Sema3c. These cells coordinate other cell types through secreted factors.

In the heart, the equivalent population is called **cardiac FAPs (cFAPs)** and is implicated in arrhythmogenic cardiomyopathy. In tendons, a distinct **T-FAP** population (Tppp3−, PDGFRα+) was found to coexist with tendon stem cells and give rise to fibrotic scar rather than new tenocytes after injury.

**Related papers:**
- [Scott et al. (2019)](papers/papers.md) — first description of FAP1/FAP2 subsets marked by Hic1 in skeletal muscle
- [Soliman et al. (2020)](papers/papers.md) — cardiac FAPs (cFAPs) in arrhythmogenic cardiomyopathy
- [Arostegui et al. (2022)](papers/papers.md) — developmental origin and fate map of FAP1/FAP2 in the limb
- [Harvey et al. (2019)](papers/papers.md) — T-FAPs in patellar tendon; their role in driving fibrosis after injury

---

### Mesenchymal Progenitors (MPs)

**What they are:** Mesenchymal progenitors are multipotent stem-like cells that can give rise to a variety of connective tissue cell types — including fibroblasts, chondrocytes (cartilage cells), osteoblasts (bone cells), adipocytes, tenocytes (tendon cells), and pericytes (blood vessel-lining cells). The term "mesenchymal" refers to the embryonic tissue layer (mesenchyme) from which connective tissues originate. "Progenitor" means these cells are one step closer to a final cell type than a true stem cell, though in practice the terms MP and stem cell are often used interchangeably in this field.

**Key features:**
- Reside in connective tissues throughout the adult body, usually in a **quiescent** (non-dividing) state
- Marked by the transcription factor **Hic1** (Hypermethylated in Cancer 1), which helps maintain their dormancy
- Activated by tissue injury; enter the cell cycle, expand, and generate progeny that rebuild damaged tissue
- Have **open chromatin** at cell-cycle gene loci even when quiescent, meaning they are "poised" to proliferate quickly

**Embryonic origin in the limb:** Hic1+ MPs in the appendicular limb arise from the **sclerotome and syndetome** compartments of the hypaxial somite (a segmented block of embryonic tissue), migrating into the developing limb bud at approximately embryonic day 11.5 (E11.5) in mice. They are distinct from and do not arise from the dermomyotome (which gives muscle) or neural crest.

**Related papers:**
- [Scott et al. (2019)](papers/papers.md) — foundational characterization of Hic1+ MPs in adult skeletal muscle
- [Arostegui et al. (2022)](papers/papers.md) — complete embryonic origin and cellular taxonomy of Hic1+ MPs in the limb
- [Arostegui et al. (2023)](papers/papers.md) — a specialized MP subset (Scx+/Sox9+) responsible for bone superstructure formation
- [Abbasi et al. (2020)](papers/papers.md) — Hic1+ MPs in skin; role in wound-induced hair follicle neogenesis
- [Soliman et al. (2020)](papers/papers.md) — Hic1+ MPs in the heart (cardiac FAPs)
- [Bernier et al. (2025)](papers/papers.md) — Hic1+ MPs (stromal progenitors) in the brain

---

### Mesenchymal Stromal Cells (MSCs)

**What they are:** "Mesenchymal stromal cell" is a broader umbrella term encompassing all stromal (non-epithelial, non-hematopoietic, non-endothelial) cells of connective tissue origin. This includes quiescent progenitors (MPs), activated/differentiated descendants, fibroblasts, pericytes, and other specialized cell types. In clinical and tissue engineering contexts, "MSCs" often specifically refers to bone marrow-derived stromal cells that are isolated, expanded in culture, and used for cell therapy, though in modern research the term is used more broadly.

**Distinction from MPs:** All MPs are MSCs, but not all MSCs are necessarily progenitors. Terminally differentiated fibroblasts, for example, are MSCs but may no longer be progenitors. In practice, Hic1+ cells in the Underhill lab's research are referred to as MSCs because Hic1 marks quiescent, progenitor-competent MSCs across many adult tissues (skeletal muscle, heart, skin, brain).

**Why the term matters:** In synovial sarcoma research, the "MSC" designation is used to describe the cell-of-origin for this cancer — a rare Hic1+ Pdgfra+ Lgr5+ MSC subpopulation whose epigenome is uniquely permissive to SS18::SSX-driven transformation.

**Related papers:**
- [Hill et al. (2025)](papers/papers.md) — MSC-specific CreERT2 targeting reveals the fibroblastic MSC origin of synovial sarcoma
- [Bernier et al. (2025)](papers/papers.md) — brain-resident MSCs (pericytes + perivascular fibroblasts) and cerebrovascular regeneration
- [Scott et al. (2019)](papers/papers.md) — Hic1 as a marker of quiescent MSCs in skeletal muscle

---

### Fibroblasts

**What they are:** Fibroblasts are the most common cell type in connective tissues. Their primary job is to produce and maintain the extracellular matrix (ECM) — the meshwork of proteins (collagen, fibronectin, proteoglycans) that provides structural support to tissues. The word "fibro-" refers to fibrous ECM, and "-blast" means a cell that creates.

**Subtypes relevant to this research:**
- **FAP1 / Dpt+ Col15a1+ fibroblasts:** ECM-enriched, structural fibroblasts found in muscle interstitium
- **FAP2 / Dpt+ Pi16+ fibroblasts:** Signaling-enriched, "universal" interstitial fibroblasts
- **Myofibroblasts (αSMA+):** Activated fibroblasts that express alpha smooth muscle actin (αSMA), contract, and deposit large amounts of collagen. Key drivers of fibrosis (scar formation) after injury
- **Fascia-resident fibroblasts, perineurial fibroblasts, perivascular fibroblasts:** Specialized subtypes found in different anatomical compartments

**Fibroblasts and scar:** After tendon or rotator cuff injury, αSMA-expressing (SMA-lineage) fibroblasts/myofibroblasts are the main contributors to the hypercellular scar tissue that fills the repair zone. This scar lacks the organized collagen structure of normal tendon and has permanently inferior mechanical properties.

**Related papers:**
- [Scott et al. (2019)](papers/papers.md) — FAP1/FAP2 fibroblast subtypes
- [Arostegui et al. (2022)](papers/papers.md) — fibroblast fates of Hic1+ MPs in the limb
- [Hill et al. (2025)](papers/papers.md) — fibroblast epigenome; Fb subtypes as synovial sarcoma cell-of-origin
- [Bernier et al. (2025)](papers/papers.md) — perivascular fibroblasts and their fibrogenic role after stroke
- [Moser et al. (2021)](papers/papers.md) — SMA-lineage fibroblasts as the dominant scar-forming cells after rotator cuff repair
- [Howell et al. (2017)](papers/papers.md) — SMA-expressing cells form permanent scar in adult (but not neonatal) tendon healing

---

### Tendon Stem/Progenitor Cells (TSPCs)

**What they are:** TSPCs are a rare population of cells in the tendon that retain the ability to self-renew and give rise to new tenocytes (tendon cells) upon injury — fulfilling the functional definition of a stem cell. They were identified in vivo relatively recently because earlier candidate populations did not hold up under rigorous genetic lineage tracing.

**Key markers and location:** The best-characterized TSPCs in paratenon-sheathed tendons (such as the patellar tendon) express **Tppp3** (tubulin polymerization-promoting protein family member 3) and **Prg4** (lubricin), and reside in the tendon sheath (paratenon) surrounding the tendon midsubstance. A fraction of Tppp3+ cells also expresses **PDGFRα** (Tppp3+Pdgfra+) — this is the subset with true stem cell function. Tppp3 expression is turned off as cells differentiate into tenocytes, allowing dual tracking with the Tppp3CG allele (identifies current Tppp3+ cells with eGFP; permanently labels their descendants with tdTomato via Cre).

**TSPCs vs T-FAPs:** In the same tendon niche, there is a separate population of **T-FAPs** (Tppp3−, PDGFRα+) — these are FAP-like cells that share PDGFRα positivity but lack Tppp3. After injury, T-FAPs differentiate into fibrotic scar cells rather than tenocytes, while TSPCs give rise to new aligned tenocytes. Both populations respond to PDGF signaling, which is why exogenous PDGF application in tendons simultaneously enhances regeneration and fibrosis.

**TSPCs and innervation:** Sensory nerves, via NGF/TrkA signaling, are required for TSPC expansion after Achilles tendon injury. When sensory innervation is blocked (e.g., by sural nerve transection), TSPC proliferation is suppressed and tendon healing is impaired.

**Related papers:**
- [Harvey et al. (2019)](papers/papers.md) — first definitive in vivo identification of Tppp3+Pdgfra+ tendon stem cells; discovery of T-FAPs
- [Cherief et al. (2023)](papers/papers.md) — sensory innervation (NGF/TrkA) is required for TSPC (Tppp3+) expansion after Achilles tendon injury

---

### Tenocytes

**What they are:** Tenocytes are the mature, specialized cells that make up the tendon midsubstance. They are highly elongated spindle-shaped cells that sit in longitudinal rows between thick parallel bundles of type I collagen (the "crimp" pattern). Their primary function is to synthesize and maintain the collagen-rich ECM that gives tendons their remarkable tensile strength.

**Key markers:** Tenocytes are identified by expression of the transcription factor **Scleraxis (Scx)**, along with **Tenomodulin (Tnmd)**, **Fibromodulin (Fmod)**, and **Thrombospondin 4 (Thbs4)**. Scx is a bHLH transcription factor that is often used to mark the tendon lineage in genetic tools (ScxGFP reporter, ScxCre, ScxCreERT2).

**Tenocytes in healing:** After adult tendon injury, tenocytes have limited regenerative capacity — they do not efficiently re-populate defect zones (unlike in neonates, where Scx-lineage cells are actively recruited into the wound). Adult Scx-lineage tenocytes may instead transdifferentiate into ectopic cartilage at injury margins. In neonatal tendon healing, TGFβ signaling directly drives tenocyte migration into the defect, and this migratory signal is required for functional repair.

**Myotenocytes:** A specialized tenocyte subtype found at the myotendinous junction (MTJ), expressing **Col22a1**, which bridges muscle and tendon. These cells emerge from Hic1+ MP progenitors.

**Related papers:**
- [Scott et al. (2019)](papers/papers.md) — Scx+ tenogenic subpopulation of Hic1+ MPs; myotenocytes at the MTJ
- [Howell et al. (2017)](papers/papers.md) — neonatal vs adult healing: Scx-lineage tenocyte recruitment in neonates
- [Harvey et al. (2019)](papers/papers.md) — tenocyte cluster in patellar tendon scRNA-seq (Fmod+, Tnmd+, Thbs4+)
- [Kaji et al. (2020)](papers/papers.md) — TGFβ signaling required for tenocyte migration during neonatal regeneration
- [Moser et al. (2021)](papers/papers.md) — loss of Scx-lineage tenocytes after supraspinatus repair; tendon degeneration
- [Arostegui et al. (2022)](papers/papers.md) — tenocyte and myotenocyte fates of Hic1+ MPs

---

## 2. Biological Processes

### Tendon Regeneration

**What it means:** Tendon regeneration refers to the process by which damaged tendon tissue is replaced by new, organized, functional tendon — not scar. True regeneration restores the original aligned collagen architecture, cell density, and mechanical properties. This is in contrast to **fibrotic repair**, where a disorganized collagenous scar replaces the defect; the scar is weaker, stiffer, and prone to re-injury.

**Why tendons are hard to regenerate:** Adult mammalian tendons have poor intrinsic regenerative capacity. After injury, the default adult response is fibrosis. The key cellular reason is that adult Scx-lineage tenocytes are not efficiently recruited back to the injury site; instead, extrinsic SMA-expressing progenitors dominate and form scar. Neonatal mice, by contrast, can regenerate full-thickness tendon defects because Scx-lineage tenocytes are still capable of active recruitment into wounds.

**Molecular drivers:** TGFβ signaling (particularly TGFβ3) acts as a chemotactic signal for tenocyte migration. Sensory nerves provide NGF/TrkA-dependent trophic support for tendon sheath progenitor (TSPC) expansion. PDGF signaling through PDGFRα on TSPCs promotes new tenocyte production — but the same signal also activates T-FAPs toward fibrosis.

**Related papers:**
- [Howell et al. (2017)](papers/papers.md) — neonatal regenerative model vs adult fibrotic healing; Scx-lineage cell recruitment
- [Kaji et al. (2020)](papers/papers.md) — TGFβ signaling required for tenocyte recruitment and neonatal tendon regeneration
- [Harvey et al. (2019)](papers/papers.md) — Tppp3+Pdgfra+ tendon stem cells regenerate patellar tendon; PDGF drives both regeneration and fibrosis
- [Moser et al. (2021)](papers/papers.md) — failure of tendon regeneration after supraspinatus repair; permanent mechanical deficits
- [Cherief et al. (2023)](papers/papers.md) — sensory innervation (TrkA) supports TSPC expansion and tendon repair

---

### Musculoskeletal Regeneration

**What it means:** Musculoskeletal regeneration is the broader process by which the entire musculoskeletal unit — muscles, tendons, ligaments, cartilage, bone, and the attachment structures between them — is repaired and restored after injury. It involves coordinated activity of multiple progenitor cell types, including muscle satellite cells (for muscle fiber repair), FAPs (for ECM remodeling and trophic support), tenocytes and TSPCs (for tendon repair), and chondro/osteoprogenitors (for bone repair).

**Attachment structures:** A key challenge in musculoskeletal regeneration is rebuilding the interfaces between tissues: the **enthesis** (tendon-to-bone attachment), the **myotendinous junction / MTJ** (muscle-to-tendon attachment), and the associated **bone superstructures** (ridges, tuberosities, eminences that anchor tendons to bone). These gradients of tissue properties are critical for stress dissipation and cannot be replicated by scar alone.

**Role of Hic1+ MPs:** The Hic1+ MP compartment is central to musculoskeletal regeneration. In skeletal muscle, Hic1+ FAPs orchestrate immune cell infiltration, vascularization, ECM production, and secretion of promyogenic cytokines. In the embryo, a specialized Hic1+ Scx+/Sox9+ progenitor subpopulation executes the "secondary wave" of bone morphogenesis that builds entheses and bone superstructures.

**Related papers:**
- [Scott et al. (2019)](papers/papers.md) — Hic1+ MPs in skeletal muscle regeneration
- [Arostegui et al. (2022)](papers/papers.md) — developmental cellular taxonomy linking embryonic MPs to adult musculoskeletal cell types
- [Arostegui et al. (2023)](papers/papers.md) — bone superstructure formation; enthesis and MTJ development; Hic1 deletion disrupts musculoskeletal coupling

---

## 3. Experimental Models

### Tendon Injury Models

Several injury models are used in mice, each with different injury severity, healing mode, and anatomical location. Choosing the right model is critical because the same species, age, and tissue can produce fundamentally different outcomes.

| Model | Tendon | Injury type | Expected healing | Used in |
|---|---|---|---|---|
| **Neonatal full-thickness patellar tendon defect** | Patellar | Complete cross-section removed | Regenerative (neo-tendon) | Howell et al. (2017), Kaji et al. (2020) |
| **Adult full-thickness patellar tendon defect** | Patellar | Complete cross-section removed | Fibrotic scar | Howell et al. (2017) |
| **Patellar tendon punch injury** | Patellar | Biopsy punch (central core removed) | Regenerative in adults | Harvey et al. (2019) |
| **Achilles tendon transection** | Achilles | Complete tendon cut | Poor, fibrotic | Kaji et al. (2020), Cherief et al. (2023) |
| **Supraspinatus tendon detachment and repair** | Supraspinatus (rotator cuff) | Full detachment + surgical repair | Permanent scar; tendon degeneration | Moser et al. (2021) |

**Key insight:** The regenerative capacity of tendon depends strongly on age (neonates regenerate, adults scar) and on the specific injury paradigm (punch injury of the patellar tendon in adults is regeneration-competent, while full transection of the Achilles is not). The patellar tendon punch model is considered the gold standard for studying adult tendon stem cell activity.

**Related papers:**
- [Howell et al. (2017)](papers/papers.md) — neonatal full-thickness patellar tendon defect; comparison with adult healing
- [Harvey et al. (2019)](papers/papers.md) — patellar tendon biopsy punch injury; Tppp3+ stem cell response
- [Kaji et al. (2020)](papers/papers.md) — neonatal patellar tendon defect; TGFβ inhibition with SB-431542
- [Moser et al. (2021)](papers/papers.md) — supraspinatus tendon detachment/repair; functional and structural assessments
- [Cherief et al. (2023)](papers/papers.md) — Achilles tendon injury; sensory denervation experiments

---

### Bone Fracture / Skeletal Injury Models

**What they are:** These are experimental methods to study how bone and its attachment structures regenerate. Rather than a single standardized model, this research uses a combination of:

- **Genetic conditional knockout (cKO):** Deleting a gene in limb mesenchyme (e.g., Prrx1-Cre; Hic1f/f) and analyzing the resulting skeletal defects by microCT and histology. This reveals what a progenitor population contributes to skeletal morphogenesis.
- **MicroCT (µCT) imaging:** X-ray-based 3D imaging of bone structure. Used to quantify cortical thickness, trabecular bone volume fraction (BV/TV), mineral density (BMD), and the presence/absence of bone protuberances and ridges.
- **Skeletal preparation (Alcian blue / Alizarin red staining):** Cartilage is stained blue and bone red to visualize overall skeletal morphology in embryos and neonates.

**What the Arostegui 2023 model revealed:** Conditional deletion of Hic1 in limb mesenchyme (Prrx1-Cre; Hic1f/f) caused specific loss of bone superstructures — the ulnar tuberosity was absent, the olecranon was thinner and shorter, and the radial tuberosity and ridges were absent — while the primary long-bone cartilage anlagen were intact. This proved that Hic1+ MPs are selectively required for the "secondary wave" of bone morphogenesis that builds the attachment structures, not the primary skeletal elements.

**Bone effects of tendon injury:** After rotator cuff tendon detachment and repair, microCT shows permanent cortical and trabecular bone loss at the humeral head enthesis, even when the tendon is surgically reattached. This demonstrates that tendon-bone mechanical coupling is required to maintain enthesis bone integrity.

**Related papers:**
- [Arostegui et al. (2023)](papers/papers.md) — Prrx1-Cre; Hic1f/f conditional knockout; loss of bone superstructures
- [Moser et al. (2021)](papers/papers.md) — microCT analysis of humeral bone loss after rotator cuff repair

---

## 4. Laboratory Methods

### Lineage Tracing (Cre-lox and CreERT2)

**The fundamental question:** Lineage tracing answers: *"Where do the cells in this tissue come from? Are these cells the descendants of a particular progenitor?"* It is the definitive method to establish the origin and fate of cell populations in living animals.

**How it works — the Cre-lox system:**

The system uses two components:
1. **Cre recombinase:** A protein (from bacteriophage P1) that cuts DNA at specific sequences called **loxP sites**. It is expressed from a promoter active in the cell type you want to track (e.g., Scleraxis-Cre marks tendon cells; Hic1-Cre marks Hic1-expressing progenitors).
2. **Reporter allele (e.g., Rosa26-tdTomato):** A gene encoding a fluorescent protein (like tdTomato, red) that is preceded by a loxP-flanked transcriptional STOP cassette. Before Cre acts, the STOP cassette blocks fluorescent protein expression. When Cre is expressed in a cell, it cuts out the STOP cassette, permanently activating the fluorescent protein in that cell and all its descendants forever.

This means: any cell that ever expressed Cre becomes permanently labeled, as do all its progeny — even if the original Cre-driving gene is later turned off.

**Tamoxifen-inducible CreERT2:**

Constitutive Cre drivers label all cells that ever expressed the target gene from development onward, which can be too broad. The **CreERT2** system adds temporal control: the Cre protein is fused to a mutated estrogen receptor ligand-binding domain (ERT2). CreERT2 is trapped in the cytoplasm until tamoxifen (or its metabolite 4-hydroxytamoxifen) is administered; tamoxifen releases it to enter the nucleus and activate recombination. This means:

- You control exactly **when** labeling occurs (e.g., label adult cells before injury vs. during healing)
- Only cells expressing the Cre driver **at the time of tamoxifen injection** are labeled

**Genetic knockouts via Cre-lox:** The same system is used to conditionally delete ("knock out") genes in specific cell types. A gene of interest is flanked by loxP sites ("floxed," e.g., Hic1f/f). When Cre is expressed, the floxed gene is excised only in Cre-expressing cells, producing a cell-type-specific knockout while other tissues are unaffected.

**Key examples in the papers:**
| Driver | Labels | Used for |
|---|---|---|
| Scx-Cre | All cells that ever expressed Scleraxis (tenocytes, tendon progenitors) | Constitutive tendon lineage tracing |
| ScxCreERT2 | Scx-expressing cells at time of tamoxifen | Adult tenocyte tracing |
| Hic1CreERT2 | Hic1+ MPs at time of tamoxifen | MP fate mapping across organs |
| SMACreERT2 | αSMA+ cells (myofibroblasts/progenitors) | Scar-forming cell tracing |
| Prrx1-Cre | Broad limb mesenchyme | Conditional knockout in limb |
| Tppp3CG | Tppp3+ sheath cells | Real-time + permanent marking of tendon stem cells |

**Related papers:**
- [Scott et al. (2019)](papers/papers.md) — Hic1CreERT2 lineage tracing in skeletal muscle
- [Arostegui et al. (2022)](papers/papers.md) — Hic1CreERT2; R26tdTomato at E10 for embryonic limb fate mapping
- [Arostegui et al. (2023)](papers/papers.md) — Hic1CT2; R26tdTom; ScxGFP triple-allele; Prrx1-Cre; Hic1f/f conditional KO
- [Howell et al. (2017)](papers/papers.md) — Scx-Cre (constitutive) tracing in neonatal vs adult patellar tendon healing
- [Harvey et al. (2019)](papers/papers.md) — Tppp3CG and Tppp3ECE alleles for TSPC fate mapping
- [Kaji et al. (2020)](papers/papers.md) — ScxGFP + non-Scx-lineage tracing in neonatal regeneration
- [Moser et al. (2021)](papers/papers.md) — ScxCreERT2 and SMACreERT2 with tamoxifen before rotator cuff injury
- [Hill et al. (2025)](papers/papers.md) — Hic1CreERT2 + conditional SS18::SSX2 allele for synovial sarcoma
- [Bernier et al. (2025)](papers/papers.md) — Hic1 fate tracking in brain after photothrombotic stroke
- [Abbasi et al. (2020)](papers/papers.md) — Hic1CreERT2 tracing in skin; Hic1f/f conditional KO

---

### Immunofluorescence (IF)

**What it is:** Immunofluorescence is a microscopy technique that uses antibodies conjugated to fluorescent dyes (fluorophores) to visualize the location of specific proteins within tissue sections. Antibodies are highly specific — they bind to one target protein (antigen). The fluorophore emits light of a specific color when excited by the right wavelength of laser or lamp, and the pattern of fluorescence reveals where the protein is expressed.

**How a typical experiment works:**
1. Tissue is fixed (e.g., in 4% paraformaldehyde) to preserve structure
2. Tissue is sectioned into thin slices (typically 10–12 µm for cryosections, 6 µm for paraffin/plastic)
3. Slices are incubated with a **primary antibody** that recognizes the target protein
4. A **secondary antibody** conjugated to a fluorophore (e.g., Cy5, Alexa-488) binds to the primary antibody
5. Nuclei are counterstained with DAPI (blue)
6. Images are acquired on a fluorescence microscope

**In the context of tendon fate mapping:** IF is used to:
- Confirm expression of marker proteins (e.g., αSMA, FMOD, Scx) at the protein level, complementing genetic lineage tracing
- Verify that Cre-recombined tdTomato-labeled cells also express the expected markers
- Reveal tissue morphology and cell organization at the cellular level (e.g., aligned vs. disorganized collagen; presence of fibrocartilage at entheses)

**Related papers:**
- [Harvey et al. (2019)](papers/papers.md) — IF for FMOD, PECAM-1, F4/80, TNC in patellar tendon sections
- [Moser et al. (2021)](papers/papers.md) — IF for αSMA in supraspinatus repair sections; combined with lineage tracing
- [Arostegui et al. (2023)](papers/papers.md) — IF for SOX9, ScxGFP, and tdTomato in embryonic forelimb sections

---

### Bulk RNA-seq

**What it is:** RNA sequencing (RNA-seq) measures the expression level of every gene in a tissue sample simultaneously. Cells transcribe their DNA into RNA molecules; the set of all RNA in a sample is called the **transcriptome**. In bulk RNA-seq, RNA from thousands to millions of cells is extracted together and sequenced, giving an average expression profile across the entire cell population.

**Steps:**
1. Extract total RNA from tissue or cells
2. Convert mRNA to complementary DNA (cDNA)
3. Fragment and sequence on a next-generation sequencer (e.g., Illumina)
4. Map reads back to the genome; count reads per gene
5. Compare gene expression between conditions (e.g., injured vs. uninjured; Hic1-deleted vs. control)

**Limitation:** Bulk RNA-seq averages signal across all cell types in the sample, so rare cell populations are diluted out by abundant cells. For example, a tendon sample mostly contains tenocytes, so the signals from rare TSPCs or FAPs will be overwhelmed. This drove the development of single-cell methods.

**Related papers:**
- [Hill et al. (2025)](papers/papers.md) — transcriptomic profiling of synovial sarcoma tumours; comparison with human SyS gene expression signatures

---

### Single-Cell RNA-seq and ATAC-seq

**Single-cell RNA-seq (scRNA-seq):**

scRNA-seq solves the bulk RNA-seq averaging problem by measuring gene expression in each individual cell separately. Tens of thousands of cells are profiled in one experiment.

**How it works (10x Chromium platform, most common):**
1. Tissue is enzymatically dissociated into a single-cell suspension
2. Cells are captured in tiny oil droplets, each containing a barcoded bead that uniquely tags all RNA from that cell
3. RNA is reverse-transcribed, amplified, and sequenced
4. Bioinformatic analysis clusters cells by similar expression profiles using dimensionality reduction (PCA, UMAP, t-SNE)
5. Each cluster is assigned a cell type identity based on known marker genes

**Key outputs:**
- **Cell clusters:** Groups of cells with similar gene expression (e.g., tenocytes, TSPCs, T-FAPs, endothelial cells)
- **Marker genes:** Genes differentially expressed in each cluster
- **UMAP/t-SNE plots:** 2D visualizations where similar cells appear close together
- **Trajectory/pseudotime analysis:** Computational inference of differentiation pathways (e.g., from progenitor to tenocyte)

**Single-cell ATAC-seq (scATAC-seq):**

While scRNA-seq measures *what genes are expressed*, scATAC-seq measures *which regions of the genome are accessible* (open chromatin). Open chromatin regions contain active promoters, enhancers, and transcription factor binding sites. Together, scRNA-seq + scATAC-seq reveal both the transcriptional state and the regulatory landscape of individual cells — allowing inference of which transcription factors drive each cell state.

**Example:** Scott et al. (2019) used both scRNA-seq and scATAC-seq on Hic1+ MPs to show that all four subpopulations (FAP1, FAP2, pericytic, tenogenic) have open chromatin at cell-cycle gene loci despite being quiescent — meaning they are epigenetically poised to proliferate quickly after injury.

**Related papers:**
- [Scott et al. (2019)](papers/papers.md) — scRNA-seq + scATAC-seq of Hic1+ MPs; identification of 4 subpopulations
- [Harvey et al. (2019)](papers/papers.md) — scRNA-seq of 2,491 patellar tendon cells; 8 clusters including TSPCs and T-FAPs
- [Arostegui et al. (2022)](papers/papers.md) — time-resolved scRNA-seq at multiple embryonic timepoints; fate mapping
- [Arostegui et al. (2023)](papers/papers.md) — scRNA-seq of 32,225 FACS-purified tdTom+ embryonic MPs; pseudotime analysis
- [Hill et al. (2025)](papers/papers.md) — transcriptomic + epigenomic profiling (H3K27me3, H2AK119ub, H3K4me3); bivalent mark analysis
- [Cherief et al. (2023)](papers/papers.md) — scRNA-seq of injured Achilles tendon with/without sensory denervation

---

### Spatial Transcriptomics (Visium and Xenium)

**The problem it solves:** scRNA-seq destroys tissue architecture — cells are dissociated from their neighbors and their original location is lost. Spatial transcriptomics (ST) methods measure gene expression while preserving the spatial position of each cell or spot within an intact tissue section.

**NGS-based ST — 10x Visium:**
- A tissue section is placed on a slide coated with spatially barcoded capture spots (55 µm diameter; ~5 µm center-to-center in Visium HD)
- mRNA from the tissue diffuses down and binds to the complementary barcoded oligonucleotides
- Captured RNA is sequenced, and each read is assigned to a spatial coordinate
- Provides the full transcriptome but at multi-cellular resolution (each spot typically contains 1–10 cells)
- Can be paired with a matched H&E-stained image of the same section

**Image-based ST — 10x Xenium:**
- RNA molecules are detected directly in intact tissue by hybridization with fluorescent probes (in situ)
- Each transcript is imaged at single-molecule resolution using sequential fluorescence rounds
- Provides true single-cell (even subcellular) resolution
- Targeted: measures a defined panel of genes (hundreds to thousands), not the full transcriptome
- Preserves spatial context of individual cells within tissue microenvironments

**Computational analysis challenges:** ST data has unique challenges: the expression matrix must be analyzed together with spatial coordinates and often histology images. This requires specialized computational methods for spatial domain identification (clustering of regions with similar expression + morphology), deconvolution (inferring cell type composition of multi-cell spots), and batch integration (combining data from multiple tissue slices). Methods such as STAIG address these challenges.

**In tendon research:** Cherief et al. (2023) used both scRNA-seq and spatial transcriptomics to characterize how sensory denervation changes the molecular environment in injured Achilles tendon, revealing disrupted TGFβ and inflammatory signaling pathways.

**Related papers:**
- [Cherief et al. (2023)](papers/papers.md) — scRNA-seq and spatial transcriptomics of injured mouse tendon; effect of denervation on signaling environment
- [Li et al. (2022)](papers/papers.md) — review of AI methods for ST analysis (SVG detection, clustering, deconvolution, enhancement)
- [Yue et al. (2023)](papers/papers.md) — comprehensive guidebook of 22 ST technologies including Visium and Xenium; 791 public datasets catalogued; 70 computational approaches
- [Yang et al. (2025)](papers/papers.md) — STAIG: deep learning for spatial domain identification using gene expression + histology images; alignment-free multi-slice integration

---

## 5. Translational Tools

### Biomaterial Scaffolds and Microphysiological Structures

**What they are:** Biomaterial scaffolds are engineered three-dimensional structures designed to support cell growth, guide tissue organization, and provide mechanical support in the context of tissue repair. They bridge the gap between laboratory discoveries (e.g., identifying TSPCs or key signaling pathways) and clinical application (e.g., improving tendon repair surgery outcomes).

**Types relevant to tendon research:**

- **Collagen scaffolds:** Since tendons are predominantly type I collagen, collagen-based scaffolds can mimic the native tendon ECM. Cells seeded onto aligned collagen fibers orient themselves longitudinally, mimicking tenocyte arrangement.
- **Decellularized ECM (dECM) scaffolds:** Tendons (or other tissues) are stripped of their cells but retain the native ECM architecture. This scaffold can then be repopulated with progenitor cells.
- **Synthetic polymer scaffolds (e.g., PLGA, PCL):** Biodegradable polymers electrospun into aligned nanofibers guide tenocyte alignment and provide tunable mechanical properties.
- **Hydrogels:** Water-swollen polymer networks that can encapsulate cells or growth factors for localized delivery to an injury site.

**Microphysiological systems (MPS) / organ-on-a-chip:**
These are miniaturized devices that recreate tissue microenvironments in vitro. For tendon research, an MPS might include:
- A 3D tendon organoid (cells embedded in aligned collagen gel between two anchor posts)
- Mechanical actuation (cyclic stretching to apply physiological strain)
- Vascular channels (to model nutrient delivery)
- Innervation (to study how nerves regulate TSPC behavior, as in the Cherief 2023 findings)

**Connection to the papers:** The fundamental biology established in these studies — the identity of TSPCs, the roles of TGFβ and NGF/TrkA, the FAP-driven fibrosis pathway — informs rational scaffold design. For example, delivering TGFβ3 locally from a scaffold could promote tenocyte migration; incorporating nerve-guidance structures could support TSPC expansion; small-molecule TrkA agonists (as tested by Cherief et al.) could be loaded into scaffolds for controlled release.

**Note:** None of the papers in this collection directly study biomaterial scaffolds; this term represents a future translational application of the basic biology described in the other papers.

**Related papers (for biological context):**
- [Kaji et al. (2020)](papers/papers.md) — TGFβ3 as a key pro-regenerative signal that could be delivered via scaffold
- [Cherief et al. (2023)](papers/papers.md) — TrkA agonist delivery improves tendon repair; translational scaffold design implication
- [Harvey et al. (2019)](papers/papers.md) — PDGF-AA promotes tenocyte production; cautionary note about concurrent fibrosis induction
