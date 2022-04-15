import os

root_folder = "Sipebi.Core"

rel_file_mapping = {
    "/Mini/SipebiMiniEditor.cs": "SipebiMini.Editor",
    "/Mini/SipebiMiniDiagnosticsReport.cs": "SipebiMini.Core",
    "/Mini/SipebiMiniParagraph.cs": "SipebiMini.Core",
    "/Mini/SipebiMiniWordDivision.cs": "SipebiMini.Core",
    "/DataModels/Diagnostics/SipebiDiagnosticsError.cs": "SipebiMini.Core",
    "/DataModels/Diagnostics/SipebiDiagnosticsErrorInformation.cs": "SipebiMini.Core",
    "/Core/SipebiWordPositionInSentence.cs": "SipebiMini.Core",
    "/Core/": "SipebiMini.Analyser",
    "/Constants/": "SipebiMini.Analyser",
    "/Extension/": "SipebiMini.Analyser",
    "/Mini/SipebiMiniAnalyser.cs": "SipebiMini.Analyser",
    "/DataModels/": "SipebiMini.Analyser",
}

file_mapping = {root_folder + k: v for (k, v) in rel_file_mapping.items()}

rel_namespace_files_list = ["/Mini/SipebiMiniEditor.cs",   "/Core/SipebiEngine.cs",       "/Core/SipebiParagraph.cs",
                            "/Core/SipebiSettings.cs",     "/Core/SipebiWordDivision.cs", "/Constants/GlobalHolder.cs",
                            "/Mini/SipebiMiniAnalyzer.cs", "/DataModels/Diagnostics/SipebiDiagnosticsError.cs"]

namespace_files_list = [root_folder + f for f in rel_namespace_files_list]

rel_excluded_files = ["/Core/SipebiAnalyser.cs",
                      "/Core/SipebiEditor.cs",
                      "/Core/SipebiWordPositionInSentence.cs",
                      "/DataModels/Diagnostics/SipebiDiagnosticsError.cs",
                      "/DataModels/Diagnostics/SipebiDiagnosticsErrorInformation.cs",
                      "/DataModels/Data/Items/Entri.cs",
                      "/DataModels/Data/Items/EntriSipebi.cs",
                      "/DataModels/Data/Items/Makna.cs",
                      "/DataModels/Data/Items/SipebiFeedback.cs",
                      "/DataModels/ApplicationPage.cs",
                      "/Constants/DataHolder.cs",
                      "/Constants/ParameterHolder.cs",
                      "/Extension/BaseExtractor.cs",
                      "/Extension/Info.cs",
                      "/Extension/MiscExtension.cs"]

excluded_files = [root_folder + f for f in rel_excluded_files]


def recurse_files(source):
    files = os.listdir(source)
    results = []
    for file in files:
        full_file_path = source + file + "/"
        if os.path.isdir(full_file_path):
            nested_files = recurse_files(full_file_path)
            results.extend(nested_files)
        else:
            results.append(full_file_path.strip("/"))

    return results


for source, destination in file_mapping.items():
    if source.endswith("/"):
        last_files = recurse_files(source)
    else:
        last_files = [source]

    for last_source in last_files:
        source_f = open(last_source)

        #Special checking? Hack?
        if destination == "SipebiMini.Analyser" and source != root_folder + "/Mini/SipebiMiniAnalyser.cs":
            if last_source in excluded_files:
                continue

            last_file_name = "/".join(last_source.split("/")[1:])
        else:
            last_file_name = last_source.split("/")[-1]

        if "_legacy" in destination or "_legacy" in last_file_name:
            continue

        destination_f = open(f"{destination}/{last_file_name}", "w")
        code = source_f.readlines()

        if last_source in namespace_files_list:
            destination_f.write("using SipebiMini.Core;\n")

        for line in code:
            if line.strip().startswith("namespace"):
                namespace = file_mapping.get(source).split("/")[0]
                destination_f.write(f"namespace {namespace} \u007b\n")
            elif line.strip().startswith("//"):
                continue
            else:
                destination_f.write(line.replace("\ufeff", ""))

