// Generated from ArmPseudo.g4 by ANTLR 4.13.2
import org.antlr.v4.runtime.tree.ParseTreeListener;

/**
 * This interface defines a complete listener for a parse tree produced by
 * {@link ArmPseudoParser}.
 */
public interface ArmPseudoListener extends ParseTreeListener {
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#program}.
	 * @param ctx the parse tree
	 */
	void enterProgram(ArmPseudoParser.ProgramContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#program}.
	 * @param ctx the parse tree
	 */
	void exitProgram(ArmPseudoParser.ProgramContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#statement}.
	 * @param ctx the parse tree
	 */
	void enterStatement(ArmPseudoParser.StatementContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#statement}.
	 * @param ctx the parse tree
	 */
	void exitStatement(ArmPseudoParser.StatementContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#assignment}.
	 * @param ctx the parse tree
	 */
	void enterAssignment(ArmPseudoParser.AssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#assignment}.
	 * @param ctx the parse tree
	 */
	void exitAssignment(ArmPseudoParser.AssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#tupleAssignment}.
	 * @param ctx the parse tree
	 */
	void enterTupleAssignment(ArmPseudoParser.TupleAssignmentContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#tupleAssignment}.
	 * @param ctx the parse tree
	 */
	void exitTupleAssignment(ArmPseudoParser.TupleAssignmentContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#tupleElements}.
	 * @param ctx the parse tree
	 */
	void enterTupleElements(ArmPseudoParser.TupleElementsContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#tupleElements}.
	 * @param ctx the parse tree
	 */
	void exitTupleElements(ArmPseudoParser.TupleElementsContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#loopStmt}.
	 * @param ctx the parse tree
	 */
	void enterLoopStmt(ArmPseudoParser.LoopStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#loopStmt}.
	 * @param ctx the parse tree
	 */
	void exitLoopStmt(ArmPseudoParser.LoopStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void enterIfStmt(ArmPseudoParser.IfStmtContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#ifStmt}.
	 * @param ctx the parse tree
	 */
	void exitIfStmt(ArmPseudoParser.IfStmtContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#condition}.
	 * @param ctx the parse tree
	 */
	void enterCondition(ArmPseudoParser.ConditionContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#condition}.
	 * @param ctx the parse tree
	 */
	void exitCondition(ArmPseudoParser.ConditionContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#block}.
	 * @param ctx the parse tree
	 */
	void enterBlock(ArmPseudoParser.BlockContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#block}.
	 * @param ctx the parse tree
	 */
	void exitBlock(ArmPseudoParser.BlockContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#functionCall}.
	 * @param ctx the parse tree
	 */
	void enterFunctionCall(ArmPseudoParser.FunctionCallContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#functionCall}.
	 * @param ctx the parse tree
	 */
	void exitFunctionCall(ArmPseudoParser.FunctionCallContext ctx);
	/**
	 * Enter a parse tree produced by the {@code IdentifierExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterIdentifierExpr(ArmPseudoParser.IdentifierExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code IdentifierExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitIdentifierExpr(ArmPseudoParser.IdentifierExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code BinaryExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterBinaryExpr(ArmPseudoParser.BinaryExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code BinaryExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitBinaryExpr(ArmPseudoParser.BinaryExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code SliceExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterSliceExpr(ArmPseudoParser.SliceExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code SliceExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitSliceExpr(ArmPseudoParser.SliceExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code IntExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterIntExpr(ArmPseudoParser.IntExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code IntExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitIntExpr(ArmPseudoParser.IntExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code ParenExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterParenExpr(ArmPseudoParser.ParenExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code ParenExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitParenExpr(ArmPseudoParser.ParenExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code FuncExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterFuncExpr(ArmPseudoParser.FuncExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code FuncExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitFuncExpr(ArmPseudoParser.FuncExprContext ctx);
	/**
	 * Enter a parse tree produced by the {@code IndexExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void enterIndexExpr(ArmPseudoParser.IndexExprContext ctx);
	/**
	 * Exit a parse tree produced by the {@code IndexExpr}
	 * labeled alternative in {@link ArmPseudoParser#expression}.
	 * @param ctx the parse tree
	 */
	void exitIndexExpr(ArmPseudoParser.IndexExprContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#slice}.
	 * @param ctx the parse tree
	 */
	void enterSlice(ArmPseudoParser.SliceContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#slice}.
	 * @param ctx the parse tree
	 */
	void exitSlice(ArmPseudoParser.SliceContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#indexList}.
	 * @param ctx the parse tree
	 */
	void enterIndexList(ArmPseudoParser.IndexListContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#indexList}.
	 * @param ctx the parse tree
	 */
	void exitIndexList(ArmPseudoParser.IndexListContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void enterArgumentList(ArmPseudoParser.ArgumentListContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#argumentList}.
	 * @param ctx the parse tree
	 */
	void exitArgumentList(ArmPseudoParser.ArgumentListContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#type}.
	 * @param ctx the parse tree
	 */
	void enterType(ArmPseudoParser.TypeContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#type}.
	 * @param ctx the parse tree
	 */
	void exitType(ArmPseudoParser.TypeContext ctx);
	/**
	 * Enter a parse tree produced by {@link ArmPseudoParser#scopedIdentifier}.
	 * @param ctx the parse tree
	 */
	void enterScopedIdentifier(ArmPseudoParser.ScopedIdentifierContext ctx);
	/**
	 * Exit a parse tree produced by {@link ArmPseudoParser#scopedIdentifier}.
	 * @param ctx the parse tree
	 */
	void exitScopedIdentifier(ArmPseudoParser.ScopedIdentifierContext ctx);
}