#include "FactExporter.h"
#include "clang/Tooling/CommonOptionsParser.h"
#include "clang/Tooling/Tooling.h"

using namespace clang;
using namespace clang::tooling;

static llvm::cl::OptionCategory Category("fact-exporter");

int main(int argc, const char **argv) {
    CommonOptionsParser options(argc, argv, Category);
    ClangTool tool(options.getCompilations(), options.getSourcePathList());

    return tool.run(newFrontendActionFactory<FactFrontendAction>().get());
}
