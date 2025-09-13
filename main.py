
import os, io, re, glob, base64
from typing import Dict, List, Optional
from PIL import Image
import streamlit as st
from streamlit.components.v1 import html as st_html
from pathlib import Path
import zipfile

def render_html(html_text: str):
    st.components.v1.html(html_text,width=40000, height=40000,scrolling=True)
    
st.set_page_config(page_title="A multi-tissue, multi-omics atlas of hypometabolism", page_icon="🧬", layout="wide")
st.markdown("""<style>.big-title{font-size:2.1rem;font-weight:800;margin:0 0 .5rem 0}.subtle{opacity:.75}.pill{display:inline-block;padding:.15rem .6rem;border-radius:999px;border:1px solid #e6ebf2;background:#fff;margin-right:.25rem}.callout{padding:.9rem 1rem;border-radius:12px;background:#f6f8fb;border:1px solid #e6ebf2}.caption{font-size:.9rem;opacity:.8}</style>""", unsafe_allow_html=True)
st.markdown('<div class="big-title">A multi-tissue, multi-omics atlas of hypometabolism</div>', unsafe_allow_html=True)
tabs = st.tabs(["Overview","Metabolome","Transcriptome","Phosphoproteome","Trans-omics network"])

    
with tabs[0]:
    c1,c2 = st.columns([1.2,1])
    with c1:
        st.markdown("""
        **What this app shows**  
        This app provides an interactive visualization of a multi‑omics atlas of induced hypometabolic states in mice:
        **Q‑neuron–induced hypometabolism (QIH)** and **fasting‑induced torpor (FIT)**.
        
        QIH mice exhibited rapid and sustained decreases in oxygen consumption (VO₂) and respiratory quotient (RQ) after CNO administration,
        whereas CNO-alone controls did not display these changes. 
        FIT mice showed a gradual reduction in VO₂ and RQ during fasting, while Ad lib controls did not.
        """)
        st.markdown("""
        **Study design**  
        • Mice were assigned to one of four experimental conditions: QIH, CNO (control for QIH, injected with clozapine-N-oxide), FIT, and Ad lib (freely fed control).  
        • Multi‑organ sampling: brain, heart, liver, kidney, skeletal muscle, brown adipose tissue (BAT), and plasma.  
        • Assays: capillary electrophoresis–mass spectrometry (metabolome), RNA‑seq (transcriptome), and liquid chromatography–mass spectrometry (phosphoproteome).  
        """)
        image = Image.open('./paper_figs/Fig1.png')
        st.image(image, caption='',use_container_width=True)
    with c2:
        st.markdown("""
        <div class="callout">
        <b>Key readouts</b><br>
        • VO₂ ↓ and RQ ↓ indicate a shift from carbohydrate to lipid oxidation, with a global reduction in energy expenditure across both models. <br>
        • Widespread metabolite changes across organs (e.g., ↑ 3‑hydroxybutyrate, ↓ lactate).<br>
        • Thousands of mRNAs significantly altered (e.g.,hypoxia-responsive genes, glycolysis, and fatty acids oxidation).<br>
        • Phosphorylation changes repress glycolysis, amino-acid metabolism, and translation, while activating lipid catabolism.<br>
        • A transcription factor module establishes positive feedback loops that coordinate metabolism, antioxidant defenses, and platelet aggregation in both QIH and FIT.
        </div>
        """, unsafe_allow_html=True)
        image = Image.open('./paper_figs/Fig2.png')
        st.image(image, caption='',use_container_width=True)
        

with tabs[1]:
    st.markdown("""
        **Study design**  
        Mice were assigned to one of four experimental conditions: QIH (Q neuron–induced hypometabolism), 
        CNO (control for QIH, injected with clozapine-N-oxide), FIT (fasting-induced torpor), and Ad lib (freely fed control). 
        After treatment, brain, heart, liver, kidney, skeletal muscle, brown adipose tissue (BAT), and plasma samples were collected 
        from each group (n = 10) for metabolomic profiling using capillary electrophoresis–mass spectrometry (CE-MS).  
        """)
    image = Image.open('./paper_figs/Fig3.png')
    st.image(image, caption='',use_container_width=True)
    
    st.markdown("""
        **Metabolic pathway**  
        The figure below shows an overview of metabolic pathways, including glycolysis/gluconeogenesis, 
        the tricarboxylic acid (TCA) cycle, and the urea cycle. Log₂ fold changes in metabolite levels are shown 
        across seven sample types under the four experimental conditions. 
        Colored triangles mark metabolites that are significantly altered (Q < 0.05) in the QIH vs CNO or FIT vs Ad lib comparisons. 
        Black crosses denote missing data for the corresponding tissue-condition pair. 
        """)
    image = Image.open('./paper_figs/Fig4.png')
    st.image(image, caption='',use_container_width=True)
    
    options1 = ['Brain',"Heart" ,"Liver","Kidney",'Muscle','BAT', 'Plasma']
    Organ= st.selectbox('Organ for visualization:',options1, key='vis1')
    image = Image.open('./paper_figs/'+Organ+'_meta.png')
    st.image(image, caption='',use_container_width=True)
    st.markdown("""
        Left panel shows the principal component analysis (PCA) plot with 95% 
        confidence ellipses of metabolite profiles. 
        Middle panels present volcano plots highlighting differentially abundant metabolites (Q < 0.05) for three pairwise comparisons: 
        QIH vs CNO, FIT vs Ad lib, and QIH vs FIT. 
        Right panels display UpSet plots that summarize the overlap of significantly increased (right) and decreased (left) metabolites 
        among the comparisons. Black boxes denote metabolites shared across comparisons, and 
        gray bars represent the total number of altered metabolites per condition.
        """)
    
    with open("list.xlsx", "rb") as f:
        st.download_button(
            label="Download the underlying data for the volcano plots",
            data=f,
            file_name="list.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="download-results-main"
        )

    with open("upset_plot.xlsx", "rb") as f:
        st.download_button(
            label="Download the underlying data for the UpSet plots",
            data=f,
            file_name="upset_plot.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="download-results-main2"
        )
                
    options2 = ['QIH vs CNO',"FIT vs Ad lib" ,"QIH vs FIT"]
    Comp= st.selectbox('Comparison for visualization:',options2, key='vis2')
    DEFAULT_HTML_PATH = Path("./omics_html/metabo_html/"+Organ+" ("+Comp+").html")
    html_text = DEFAULT_HTML_PATH.read_text(encoding="utf-8", errors="ignore")
    render_html(html_text)
    
    
with tabs[2]:
    st.markdown("""
        **Study design**  
        Mice were assigned to one of four experimental conditions: QIH (Q neuron–induced hypometabolism), 
        CNO (control for QIH, injected with clozapine-N-oxide), FIT (fasting-induced torpor), and Ad lib (freely fed control). 
        Liver and skeletal muscle were collected after 10 hours of intervention (n = 10 per group) 
        for transcriptome analysis using RNA sequencing (RNA-seq).  
        """)
    image = Image.open('./paper_figs/Fig5.png')
    st.image(image, caption='',use_container_width=True)
    
    options3 = ["Liver",'Muscle']
    Organ= st.selectbox('Organ for visualization:',options3, key='vis3')
    image = Image.open('./paper_figs/'+Organ+'_tra.png')
    st.image(image, caption='',use_container_width=True)
    st.markdown("""
        Left panel shows the principal component analysis (PCA) plot with 95% 
        confidence ellipses of transcriptomic profiles. 
        Middle panels present MA plots highlighting differentially expressed genes (Q < 0.01) for three pairwise comparisons: 
        QIH vs CNO, FIT vs Ad lib, and QIH vs FIT. 
        Right panels display UpSet plots that summarize the overlap of significantly increased (right) and decreased (left) genes 
        among the comparisons. Black boxes denote genes shared across comparisons, and 
        gray bars represent the total number of altered genes per condition.
        """)
    
    with open("list.xlsx", "rb") as f:
        st.download_button(
            label="Download the underlying data for the MA plots",
            data=f,
            file_name="list.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="download-results-main3"
        )

    with open("upset_plot.xlsx", "rb") as f:
        st.download_button(
            label="Download the underlying data for the UpSet plots",
            data=f,
            file_name="upset_plot.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="download-results-main4"
        )
                
    options2 = ['QIH vs CNO',"FIT vs Ad lib" ,"QIH vs FIT"]
    Comp= st.selectbox('Comparison for visualization:',options2, key='vis4')
    DEFAULT_HTML_PATH = Path("./omics_html/tran_html/"+Organ+" ("+Comp+").html")
    html_text = DEFAULT_HTML_PATH.read_text(encoding="utf-8", errors="ignore")
    render_html(html_text)

with tabs[3]:
    st.markdown("""
        **Study design**  
        Mice were assigned to one of four experimental conditions: QIH (Q neuron–induced hypometabolism), 
        CNO (control for QIH, injected with clozapine-N-oxide), FIT (fasting-induced torpor), and Ad lib (freely fed control). 
        Liver and skeletal muscle samples were collected after 10 hours of intervention (n = 10 per group) 
        and subjected to phosphoproteomic analysis using liquid chromatography–mass spectrometry (LC-MS).   
        """)
    image = Image.open('./paper_figs/Fig6.png')
    st.image(image, caption='',use_container_width=True)
    
    options4 = ["Liver",'Muscle']
    Organ= st.selectbox('Organ for visualization:',options4, key='vis5')
    image = Image.open('./paper_figs/'+Organ+'_pho.png')
    st.image(image, caption='',use_container_width=True)
    st.markdown("""
        Left panel shows the principal component analysis (PCA) plot with 95% 
        confidence ellipses of phosphoproteome profiles. 
        Middle panels present volcano plots highlighting significantly altered phosphorylation sites (Q < 0.05) for three pairwise comparisons: 
        QIH vs CNO, FIT vs Ad lib, and QIH vs FIT. 
        Right panels display UpSet plots that summarize the overlap of significantly increased (right) and decreased (left) phosphorylation sites 
        among the comparisons. Black boxes denote phosphosites shared across comparisons, and 
        gray bars represent the total number of altered phosphosites per condition.
        """)
    
    with open("list.xlsx", "rb") as f:
        st.download_button(
            label="Download the underlying data for the volcano plots",
            data=f,
            file_name="list.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="download-results-main5"
        )

    with open("upset_plot.xlsx", "rb") as f:
        st.download_button(
            label="Download the underlying data for the UpSet plots",
            data=f,
            file_name="upset_plot.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="download-results-main6"
        )
                
    options2 = ['QIH vs CNO',"FIT vs Ad lib" ,"QIH vs FIT"]
    Comp= st.selectbox('Comparison for visualization:',options2, key='vis6')
    DEFAULT_HTML_PATH = Path("./omics_html/phospho_html/"+Organ+" ("+Comp+").html")
    html_text = DEFAULT_HTML_PATH.read_text(encoding="utf-8", errors="ignore")
    render_html(html_text)
    
with tabs[4]:
    st.markdown("""
        **Study design**  
        Extracellular ligands and metabolites regulate intracellular signaling pathways through receptors and transporters. 
        These signaling cascades influence transcription factor activities, which modulate the expression of enzymes and transporters 
        that control metabolism. Metabolic reactions are also shaped by substrate/product concentrations and allosteric regulation by metabolites.
        Additionally, metabolites can be transported across organs through inter-organ exchange.
        To uncover such molecular networks underlying hypometabolic states, we constructed trans-omics networks by integrating 
        metabolomic, transcriptomic, and phosphoproteomic datasets. 
        We then analyzed the network architecture based on topological features, such as degree distribution and motif structures.  
        """)
    image = Image.open('./paper_figs/Fig7.png')
    st.image(image, caption='',use_container_width=True)

    st.markdown("""
        **Trans-omics networks**  
        Trans-omics networks connecting the liver (left), blood (center), and skeletal muscle (right) for the QIH (upper) and FIT (lower) conditions.
        Nodes represent molecules (e.g., mRNAs, proteins, metabolites), and edges denote inferred regulatory relationships. 
        Edge color denotes the directionality of molecular change relative to the control condition: cyan for QIH-upregulated, 
        green for QIH-downregulated, blue for FIT-upregulated, and red for FIT-downregulated. 
        Numeric annotations show the number of regulated elements within and between each molecular layer 
        (e.g., transcription factors, transporters, enzymes, reactions, and metabolites).  
        """)
    image = Image.open('./paper_figs/Fig8.png')
    st.image(image, caption='',use_container_width=True)
    
    
    st.markdown("""
        **Positive feedback subnetworks extracted from the trans-omics networks in QIH and FIT**  
        All mRNAs in the networks increased significantly in QIH or FIT. 
        Bar plots show the number of downstream molecular targets regulated by each gene circuit.  
        """)
    image = Image.open('./paper_figs/Fig9.png')
    st.image(image, caption='',use_container_width=True)

    with open("network.xlsx", "rb") as f:
        st.download_button(
            label="Download the underlying data for the trans-omics networks",
            data=f,
            file_name="network.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",key="download-results-main8"
        )