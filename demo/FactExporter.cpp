#include "FactExporter.h"
#include "clang/AST/ASTContext.h"
#include "clang/AST/Expr.h"
#include "clang/Lex/Lexer.h"
#include "llvm/Support/raw_ostream.h"

using namespace clang;

FactVisitor::FactVisitor(ASTContext *context)
    : Context(context),
      loopFile("loop_stmt.facts"),
      lengthFile("loop_length.facts"),
      assignFile("array_assign.facts"),
      typeFile("array_type.facts") {}

bool FactVisitor::VisitFunctionDecl(FunctionDecl *FD) {
    if (FD->hasBody()) {
        currentFunction = FD->getNameAsString();
        for (const ParmVarDecl *param : FD->parameters()) {
            if (param->getType()->isPointerType()) {
                const QualType elemType = param->getType()->getPointeeType();
                varTypes[param->getNameAsString()] = elemType.getAsString();
                typeFile << param->getNameAsString() << "\t" << elemType.getAsString() << "\n";
            }
        }
    }
    return true;
}

bool FactVisitor::VisitForStmt(ForStmt *FS) {
    std::string loopId = "loop" + std::to_string(++loopCounter);
    writeLoopInfo(loopId);
    writeLoopLength(FS, loopId);
    return true;
}

void FactVisitor::writeLoopInfo(const std::string &loopId) {
    loopFile << currentFunction << "\t" << loopId << "\n";
}

void FactVisitor::writeLoopLength(ForStmt *FS, const std::string &loopId) {
    if (auto *cond = dyn_cast<BinaryOperator>(FS->getCond())) {
        if (cond->getOpcode() == BO_LT) {
            if (auto *rhs = dyn_cast<IntegerLiteral>(cond->getRHS())) {
                uint64_t val = rhs->getValue().getLimitedValue();
                lengthFile << currentFunction << "\t" << loopId << "\t" << val << "\n";
            }
        }
    }
}

bool FactVisitor::VisitBinaryOperator(BinaryOperator *BO) {
    if (!BO->isAssignmentOp()) return true;

    auto *lhs = BO->getLHS(), *rhs = BO->getRHS();
    auto *lhsArr = dyn_cast<ArraySubscriptExpr>(lhs);
    auto *rhsBin = dyn_cast<BinaryOperator>(rhs);
    if (!lhsArr || !rhsBin || rhsBin->getOpcode() != BO_Add) return true;

    auto *a1 = dyn_cast<ArraySubscriptExpr>(rhsBin->getLHS());
    auto *a2 = dyn_cast<ArraySubscriptExpr>(rhsBin->getRHS());
    if (!a1 || !a2) return true;

    std::string C = Lexer::getSourceText(CharSourceRange::getTokenRange(lhsArr->getBase()->getSourceRange()),
                                         *Context->getSourceManager(), LangOptions(), 0).str();
    std::string A = Lexer::getSourceText(CharSourceRange::getTokenRange(a1->getBase()->getSourceRange()),
                                         *Context->getSourceManager(), LangOptions(), 0).str();
    std::string B = Lexer::getSourceText(CharSourceRange::getTokenRange(a2->getBase()->getSourceRange()),
                                         *Context->getSourceManager(), LangOptions(), 0).str();

    assignFile << currentFunction << "\t0\t" << C << "\t" << A << "\t" << B << "\t+\n";
    return true;
}

void FactVisitor::dumpFacts() {
    loopFile.close();
    lengthFile.close();
    assignFile.close();
    typeFile.close();
}

FactConsumer::FactConsumer(ASTContext *context) : Visitor(context) {}

void FactConsumer::HandleTranslationUnit(ASTContext &context) {
    Visitor.TraverseDecl(context.getTranslationUnitDecl());
    Visitor.dumpFacts();
}

std::unique_ptr<ASTConsumer> FactFrontendAction::CreateASTConsumer(CompilerInstance &CI, StringRef InFile) {
    return std::make_unique<FactConsumer>(&CI.getASTContext());
}
