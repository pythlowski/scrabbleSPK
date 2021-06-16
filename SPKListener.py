# Generated from SPK.g4 by ANTLR 4.9.2
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .SPKParser import SPKParser
else:
    from SPKParser import SPKParser

# This class defines a complete listener for a parse tree produced by SPKParser.
class SPKListener(ParseTreeListener):

    # Enter a parse tree produced by SPKParser#program.
    def enterProgram(self, ctx:SPKParser.ProgramContext):
        pass

    # Exit a parse tree produced by SPKParser#program.
    def exitProgram(self, ctx:SPKParser.ProgramContext):
        pass


    # Enter a parse tree produced by SPKParser#bigStmt.
    def enterBigStmt(self, ctx:SPKParser.BigStmtContext):
        pass

    # Exit a parse tree produced by SPKParser#bigStmt.
    def exitBigStmt(self, ctx:SPKParser.BigStmtContext):
        pass


    # Enter a parse tree produced by SPKParser#if_stat.
    def enterIf_stat(self, ctx:SPKParser.If_statContext):
        pass

    # Exit a parse tree produced by SPKParser#if_stat.
    def exitIf_stat(self, ctx:SPKParser.If_statContext):
        pass


    # Enter a parse tree produced by SPKParser#while_stat.
    def enterWhile_stat(self, ctx:SPKParser.While_statContext):
        pass

    # Exit a parse tree produced by SPKParser#while_stat.
    def exitWhile_stat(self, ctx:SPKParser.While_statContext):
        pass


    # Enter a parse tree produced by SPKParser#for_loop.
    def enterFor_loop(self, ctx:SPKParser.For_loopContext):
        pass

    # Exit a parse tree produced by SPKParser#for_loop.
    def exitFor_loop(self, ctx:SPKParser.For_loopContext):
        pass


    # Enter a parse tree produced by SPKParser#print_.
    def enterPrint_(self, ctx:SPKParser.Print_Context):
        pass

    # Exit a parse tree produced by SPKParser#print_.
    def exitPrint_(self, ctx:SPKParser.Print_Context):
        pass


    # Enter a parse tree produced by SPKParser#range_.
    def enterRange_(self, ctx:SPKParser.Range_Context):
        pass

    # Exit a parse tree produced by SPKParser#range_.
    def exitRange_(self, ctx:SPKParser.Range_Context):
        pass


    # Enter a parse tree produced by SPKParser#condition_block.
    def enterCondition_block(self, ctx:SPKParser.Condition_blockContext):
        pass

    # Exit a parse tree produced by SPKParser#condition_block.
    def exitCondition_block(self, ctx:SPKParser.Condition_blockContext):
        pass


    # Enter a parse tree produced by SPKParser#condition.
    def enterCondition(self, ctx:SPKParser.ConditionContext):
        pass

    # Exit a parse tree produced by SPKParser#condition.
    def exitCondition(self, ctx:SPKParser.ConditionContext):
        pass


    # Enter a parse tree produced by SPKParser#block.
    def enterBlock(self, ctx:SPKParser.BlockContext):
        pass

    # Exit a parse tree produced by SPKParser#block.
    def exitBlock(self, ctx:SPKParser.BlockContext):
        pass


    # Enter a parse tree produced by SPKParser#fblock.
    def enterFblock(self, ctx:SPKParser.FblockContext):
        pass

    # Exit a parse tree produced by SPKParser#fblock.
    def exitFblock(self, ctx:SPKParser.FblockContext):
        pass


    # Enter a parse tree produced by SPKParser#function_.
    def enterFunction_(self, ctx:SPKParser.Function_Context):
        pass

    # Exit a parse tree produced by SPKParser#function_.
    def exitFunction_(self, ctx:SPKParser.Function_Context):
        pass


    # Enter a parse tree produced by SPKParser#returnable.
    def enterReturnable(self, ctx:SPKParser.ReturnableContext):
        pass

    # Exit a parse tree produced by SPKParser#returnable.
    def exitReturnable(self, ctx:SPKParser.ReturnableContext):
        pass


    # Enter a parse tree produced by SPKParser#function_exec.
    def enterFunction_exec(self, ctx:SPKParser.Function_execContext):
        pass

    # Exit a parse tree produced by SPKParser#function_exec.
    def exitFunction_exec(self, ctx:SPKParser.Function_execContext):
        pass


    # Enter a parse tree produced by SPKParser#arguments.
    def enterArguments(self, ctx:SPKParser.ArgumentsContext):
        pass

    # Exit a parse tree produced by SPKParser#arguments.
    def exitArguments(self, ctx:SPKParser.ArgumentsContext):
        pass


    # Enter a parse tree produced by SPKParser#arguments_exec.
    def enterArguments_exec(self, ctx:SPKParser.Arguments_execContext):
        pass

    # Exit a parse tree produced by SPKParser#arguments_exec.
    def exitArguments_exec(self, ctx:SPKParser.Arguments_execContext):
        pass


    # Enter a parse tree produced by SPKParser#declaration.
    def enterDeclaration(self, ctx:SPKParser.DeclarationContext):
        pass

    # Exit a parse tree produced by SPKParser#declaration.
    def exitDeclaration(self, ctx:SPKParser.DeclarationContext):
        pass


    # Enter a parse tree produced by SPKParser#assignment.
    def enterAssignment(self, ctx:SPKParser.AssignmentContext):
        pass

    # Exit a parse tree produced by SPKParser#assignment.
    def exitAssignment(self, ctx:SPKParser.AssignmentContext):
        pass


    # Enter a parse tree produced by SPKParser#break_.
    def enterBreak_(self, ctx:SPKParser.Break_Context):
        pass

    # Exit a parse tree produced by SPKParser#break_.
    def exitBreak_(self, ctx:SPKParser.Break_Context):
        pass


    # Enter a parse tree produced by SPKParser#sleep_.
    def enterSleep_(self, ctx:SPKParser.Sleep_Context):
        pass

    # Exit a parse tree produced by SPKParser#sleep_.
    def exitSleep_(self, ctx:SPKParser.Sleep_Context):
        pass


    # Enter a parse tree produced by SPKParser#expr.
    def enterExpr(self, ctx:SPKParser.ExprContext):
        pass

    # Exit a parse tree produced by SPKParser#expr.
    def exitExpr(self, ctx:SPKParser.ExprContext):
        pass


    # Enter a parse tree produced by SPKParser#atom.
    def enterAtom(self, ctx:SPKParser.AtomContext):
        pass

    # Exit a parse tree produced by SPKParser#atom.
    def exitAtom(self, ctx:SPKParser.AtomContext):
        pass


    # Enter a parse tree produced by SPKParser#iterable.
    def enterIterable(self, ctx:SPKParser.IterableContext):
        pass

    # Exit a parse tree produced by SPKParser#iterable.
    def exitIterable(self, ctx:SPKParser.IterableContext):
        pass


    # Enter a parse tree produced by SPKParser#list_element.
    def enterList_element(self, ctx:SPKParser.List_elementContext):
        pass

    # Exit a parse tree produced by SPKParser#list_element.
    def exitList_element(self, ctx:SPKParser.List_elementContext):
        pass


    # Enter a parse tree produced by SPKParser#list_values.
    def enterList_values(self, ctx:SPKParser.List_valuesContext):
        pass

    # Exit a parse tree produced by SPKParser#list_values.
    def exitList_values(self, ctx:SPKParser.List_valuesContext):
        pass


    # Enter a parse tree produced by SPKParser#list_index.
    def enterList_index(self, ctx:SPKParser.List_indexContext):
        pass

    # Exit a parse tree produced by SPKParser#list_index.
    def exitList_index(self, ctx:SPKParser.List_indexContext):
        pass



del SPKParser