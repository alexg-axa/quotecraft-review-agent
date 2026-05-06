from __future__ import annotations

import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent

from main import (
    SYSTEM_PROMPT,
    USER_PROMPT,
    build_evidence_inventory,
    collect_review_evidence,
    create_model,
    extract_final_content,
    get_app_repo_path,
    get_case_materials_path,
    list_evidence_sources,
    save_evidence_inventory,
    save_markdown_report,
    save_pdf_report,
    validate_paths,
)


def run_review(output_dir: Path, generate_pdf: bool) -> tuple[str, Path, Path | None]:
    agent = create_agent(
        model=create_model(),
        tools=[list_evidence_sources, collect_review_evidence],
        system_prompt=SYSTEM_PROMPT,
    )
    response = agent.invoke({"messages": [{"role": "user", "content": USER_PROMPT}]})
    report = extract_final_content(response)
    markdown_path = save_markdown_report(report, output_dir)
    pdf_path = save_pdf_report(report, output_dir) if generate_pdf else None
    return report, markdown_path, pdf_path


def set_review_paths(repo_path: Path, case_materials_path: Path) -> None:
    os.environ["QUOTECRAFT_REPO_PATH"] = str(repo_path)
    os.environ["CASE_MATERIALS_PATH"] = str(case_materials_path)


def main() -> None:
    load_dotenv()

    st.set_page_config(page_title="QuoteCraft Review Agent", layout="wide")
    st.title("QuoteCraft Review Agent")
    st.caption("Local LangChain ReAct-style architecture review agent")

    with st.sidebar:
        st.header("Inputs")
        repo_path = Path(
            st.text_input("QuoteCraft repo path", value=str(get_app_repo_path()))
        ).resolve()
        case_materials_path = Path(
            st.text_input("Case materials path", value=str(get_case_materials_path()))
        ).resolve()
        output_dir = Path(st.text_input("Output directory", value="outputs")).resolve()
        generate_pdf = st.checkbox("Generate PDF", value=True)

        st.header("Actions")
        list_clicked = st.button("List Evidence", use_container_width=True)
        run_clicked = st.button("Run Review", type="primary", use_container_width=True)

    inventory_tab, report_tab, files_tab = st.tabs(
        ["Evidence Inventory", "Findings Report", "Output Files"]
    )

    try:
        validate_paths(repo_path, case_materials_path)
    except RuntimeError as error:
        st.error(str(error))
        return

    if list_clicked:
        set_review_paths(repo_path, case_materials_path)
        inventory = build_evidence_inventory(repo_path, case_materials_path)
        inventory_path = save_evidence_inventory(inventory, output_dir)
        with inventory_tab:
            st.markdown("### Evidence Inventory")
            st.code(inventory, language="text")
        with files_tab:
            st.success(f"Saved evidence inventory: {inventory_path}")

    if run_clicked:
        set_review_paths(repo_path, case_materials_path)
        inventory = build_evidence_inventory(repo_path, case_materials_path)
        inventory_path = save_evidence_inventory(inventory, output_dir)

        with st.spinner("Running architecture review..."):
            report, markdown_path, pdf_path = run_review(output_dir, generate_pdf)

        with inventory_tab:
            st.markdown("### Evidence Inventory")
            st.code(inventory, language="text")

        with report_tab:
            st.markdown(report)

        with files_tab:
            st.success(f"Saved evidence inventory: {inventory_path}")
            st.success(f"Saved Markdown report: {markdown_path}")
            if pdf_path:
                st.success(f"Saved PDF report: {pdf_path}")
            else:
                st.info("PDF generation skipped.")


if __name__ == "__main__":
    main()
