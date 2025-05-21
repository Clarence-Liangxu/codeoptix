#pragma once
#include "clang/AST/RecursiveASTVisitor.h"
#include "clang/Frontend/FrontendActions.h"
#include "clang/Frontend/CompilerInstance.h"
#include "clang/Tooling/Tooling.h"
#include <fstream>
#include <string>
#include <unordered_map>

using namespace clang;

class FactVisitor : public RecursiveASTVisitor<FactVisitor> {
public:
    explicit FactVisitor(ASTContext *context);
    bool VisitFunctionDecl(FunctionDecl *FD);
    bool VisitForStmt(ForStmt *FS);
    bool VisitBinaryOperator(BinaryOperator *BO);
    void dumpFacts();

private:
    ASTContext *Context;
    std::string currentFunction;
    int loopCounter = 0;

    std::ofstream loopFile, lengthFile, assignFile, typeFile;
    std::unordered_map<std::string, std::string> varTypes;

    void writeLoopInfo(const std::string &loopId);
    void writeAssign(BinaryOperator *BO, const std::string &loopId);
    void writeLoopLength(ForStmt *FS, const std::string &loopId);
};

class FactConsumer : public ASTConsumer {
public:
    explicit FactConsumer(ASTContext *context);
    void HandleTranslationUnit(ASTContext &context) override;

private:
    FactVisitor Visitor;
};

class FactFrontendAction : public ASTFrontendAction {
public:
    std::unique_ptr<ASTConsumer> CreateASTConsumer(CompilerInstance &CI, StringRef InFile) override;
};
