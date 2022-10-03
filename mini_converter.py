import os
import argparse

parser = argparse.ArgumentParser(
    description="Insert the correct source and destination folders"
)
parser.add_argument(
    "--source_folder",
    type=str,
    default="C:/ASTrio/VS2017/Desktop/Sipebi/Sipebi.Core",
    help="Source folder for Sipebi",
)
parser.add_argument(
    "--dest_folder",
    type=str,
    default="C:/ASTrio/VS2017/Desktop/Sipebi",
    help="Destination folder for Sipebi Mini",
)
args = parser.parse_args()

source_folder = args.source_folder
dest_folder = args.dest_folder

rel_file_mapping = {
    # Bug?? Completely deleted??
    "/Mini/SipebiMiniEditor.cs": "SipebiMini.Editor",
    "/Mini/SipebiMiniDiagnosticsReport.cs": "SipebiMini.Core",
    "/Mini/SipebiMiniParagraph.cs": "SipebiMini.Core",
    "/Mini/SipebiMiniWordDivision.cs": "SipebiMini.Core",
    "/DataModels/Diagnostics/SipebiDiagnosticsError.cs": "SipebiMini.Core",
    # Bug?? namespace is changed from Sipebi.Core to SipebiMini.Core
    "/DataModels/Diagnostics/SipebiDiagnosticsErrorInformation.cs": "SipebiMini.Core",  # noqa
    "/Core/SipebiWordPositionInSentence.cs": "SipebiMini.Core",
    "/Core/": "SipebiMini.Analyser",
    "/Constants/": "SipebiMini.Analyser",
    "/Extension/": "SipebiMini.Analyser",
    "/Mini/SipebiMiniAnalyser.cs": "SipebiMini.Analyser",
    "/DataModels/": "SipebiMini.Analyser",
}

file_mapping = {source_folder + k: v for (k, v) in rel_file_mapping.items()}

rel_namespace_files_list = [
    "/Mini/SipebiMiniEditor.cs",
    "/Core/SipebiEngine.cs",
    "/Core/SipebiParagraph.cs",
    "/Core/SipebiSettings.cs",
    "/Core/SipebiWordDivision.cs",
    "/Constants/GlobalHolder.cs",
    "/Mini/SipebiMiniAnalyser.cs",
    "/DataModels/Diagnostics/SipebiDiagnosticsError.cs",
    "/DataModels/Diagnostics/SipebiParagraphDiagnosticsReport.cs",
    "/DataModels/Diagnostics/SipebiDiagnosticsReport.cs",
]

namespace_files_list = [source_folder + f for f in rel_namespace_files_list]

rel_excluded_files = [
    "/Core/SipebiAnalyser.cs",
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
    "/Extension/MiscExtension.cs",
]

excluded_files = [source_folder + f for f in rel_excluded_files]


def recurse_files(source):
    files = os.listdir(source)
    results = []
    for file in files:
        full_file_path = source + file + "/"
        if os.path.isdir(full_file_path):
            nested_files = recurse_files(full_file_path)
            results.extend(nested_files)
        else:
            results.append(full_file_path.rstrip("/"))

    return results


# The making must either be completed correctly, or else
# it should not be performed at all.
# Otherwise, it may result in "broken" files

# Source can be a single file, or if it is a folder, it will be
# recursively searched nestedly
# Looks OK. But not sure if a folder should always be recursively searched
list_last_files = []
for source, destination in file_mapping.items():
    last_files = recurse_files(source) if source.endswith("/") else [source]
    list_last_files.extend(last_files)

    for last_source in last_files:
        source_f = open(last_source)

        last_file_name = ""
        # Special checking? Hack?
        # In case folders are taken, then exclude some items,
        # but why having conditions below?
        # So, SipebiAnalyser folder is apparently treated differently
        # (having multiple name parts)

        if (
            destination == "SipebiMini.Analyser"
            and source != source_folder + "/Mini/SipebiMiniAnalyser.cs"
        ):
            if last_source in excluded_files:
                continue
            # BUGGGGG!!!!!!!!!
            # !! Discounting the first element!
            # But this will only work if the first element is
            # always assumed to be Sipebi.Core!
            # last_file_name = "/".join(last_source.split("/")[1:])

            # i.e:
            # Do/Not/Use/Such/Cheat/In
            # /Coding/Core/SipebiConjunctionSubDivision.cs can be the last name
            # that originally comes from
            # C:/Do/Not/Use/Such/Cheat/In/Coding
            # /Core/SipebiConjunctionSubDivision.cs
            # But the real, desired, last name is
            # Core/SipebiConjunctionSubDivision.cs
            # the way to do it, is by taking the relative path and then adds
            # with whatever addition elements which exist after
            # the relative path
            last_file_name = last_source[len(source_folder) : len(last_source)]  # noqa
        else:
            last_file_name = last_source.split("/")[-1]

        # _legacy folders or files are skipped
        if "_legacy" in destination or "_legacy" in last_file_name:
            continue

        # If destination folder is not empty, then use it + /,
        # otherwise do not put any prefix in the destination folder
        dest_prefix = (dest_folder + "/") if dest_folder else ""
        destination_f = open(
            f"{dest_prefix}{destination}/{last_file_name}", "w"
        )  # noqa
        code = source_f.readlines()

        # Collection of files requiring additional 'using SipebiMini.Core;'
        # at the beginning of the file
        if last_source in namespace_files_list:
            destination_f.write("using SipebiMini.Core;\n")

        for line in code:
            line = line.replace("\ufeff", "")
            if line.strip().startswith("namespace"):
                namespace = destination.split("/")[0]
                # supposedly printing 'namespace SipebiMini.Core {',
                # but it maybe mistaken to '...Sipebi.Core {'
                destination_f.write(f"namespace {namespace} \u007b\n")
            # comment removal, only at the beginning of a line though
            elif "SipebiSettings.cs" in last_file_name and "PH" in line:
                line = line.replace("PH", "MDH")
                line = line.replace("SipebiReP", "SipebiMiniP")
                line = line.replace("SipebiReK", "SipebiMiniK")
                destination_f.write(line)
            elif line.strip().startswith("//"):
                continue
            else:
                destination_f.write(line)
