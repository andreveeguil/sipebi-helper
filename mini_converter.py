import os

file_mapping = {
    "Sipebi.Core/Mini/SipebiMiniEditor.cs": "SipebiMini.Editor",
    "Sipebi.Core/Mini/SipebiMiniDiagnosticsReport.cs": "SipebiMini.Core",
    "Sipebi.Core/Mini/SipebiMiniParagraph.cs": "SipebiMini.Core",
    "Sipebi.Core/Mini/SipebiMiniWordDivision.cs": "SipebiMini.Core",
    "Sipebi.Core/DataModels/Diagnostics/SipebiDiagnosticsError.cs": "SipebiMini.Core",
    "Sipebi.Core/DataModels/Diagnostics/SipebiDiagnosticsErrorInformation.cs": "SipebiMini.Core",
    "Sipebi.Core/Core/SipebiWordPositionInSentence.cs": "SipebiMini.Core",
    "Sipebi.Core/Core/": "SipebiMini.Analyser",
    "Sipebi.Core/Constants/": "SipebiMini.Analyser",
    "Sipebi.Core/Extension/": "SipebiMini.Analyser",
    "Sipebi.Core/Mini/SipebiMiniAnalyser.cs": "SipebiMini.Analyser",
    "Sipebi.Core/DataModels/": "SipebiMini.Analyser",
}

namespace_files_list = ["Sipebi.Core/Mini/SipebiMiniEditor.cs", "Sipebi.Core/Core/SipebiEngine.cs", "Sipebi.Core/Core/SipebiParagraph.cs",
                        "Sipebi.Core/Core/SipebiSettings.cs", "Sipebi.Core/Core/SipebiWordDivision.cs", "Sipebi.Core/Constants/GlobalHolder.cs",
                        "Sipebi.Core/Mini/SipebiMiniAnalyzer.cs", "Sipebi.Core/DataModels/Diagnostics/SipebiDiagnosticsError.cs"]

excluded_files = ["Sipebi.Core/Core/SipebiAnalyser.cs", "Sipebi.Core/Core/SipebiEditor.cs", "Sipebi.Core/Core/SipebiWordPositionInSentence.cs",
                  "Sipebi.Core/DataModels/Diagnostics/SipebiDiagnosticsError.cs", "Sipebi.Core/DataModels/Diagnostics/SipebiDiagnosticsErrorInformation.cs",
                  "Sipebi.Core/DataModels/Data/Items/Entri.cs", "Sipebi.Core/DataModels/Data/Items/EntriSipebi.cs",
                  "Sipebi.Core/DataModels/Data/Items/Makna.cs", "Sipebi.Core/DataModels/Data/Items/SipebiFeedback.cs",
                  "Sipebi.Core/DataModels/ApplicationPage.cs", "Sipebi.Core/Constants/DataHolder.cs", "Sipebi.Core/Constants/ParameterHolder.cs",
                  "Sipebi.Core/Extension/BaseExtractor.cs", "Sipebi.Core/Extension/Info.cs", "Sipebi.Core/Extension/MiscExtension.cs"]


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
        if destination == "SipebiMini.Analyser" and source != "Sipebi.Core/Mini/SipebiMiniAnalyser.cs":
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

