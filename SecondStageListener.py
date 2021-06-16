from SPKListener import SPKListener
from SPKParser import SPKParser
import time

class ExceptionSPK(Exception):
    # pass
    def __init__(self, message, line):
        self.message = message
        self.line = line

    def __str__(self):
        return f"BŁĄD! Linia {self.line}: {self.message}"


class SecondStageListener(SPKListener):

    def __init__(self, functions_data, walker):
        self.memory = {
            'functions': functions_data,
            'scopes': [{}]
        }
        self.walker = walker
        self.skipping = False
        self.skipExpr = False
        self.skipBlock = False
        self.skipCondition = False
        self.skipFBlock = False
        self.break_on = False
        self.inside_loop = False
        self.latest_function_result = {'name': None, 'value': None}
        self.for_loop_level = 0
        self.while_loop_level = 0
        self.if_loop_level = 0
        # print('SECOND STAGE')

    def exitDeclaration(self, ctx: SPKParser.DeclarationContext):  # CALKOWITA x = 2;
        if not self.skipping and not self.skipFBlock:
            if ctx.VARIABLE_NAME() not in self.memory['scopes'][-1].keys():
                type_name = str(ctx.TYPE_NAME())
                value = ctx.expr().result
                if correct_type(type_name, value):
                    self.memory['scopes'][-1][str(ctx.VARIABLE_NAME())] = {'type': type_name, 'value': value}
                else:
                    raise ExceptionSPK(f'Brak zgodności typów danych w deklaracji zmiennej. Podano zmienną typu {get_type_SPK(type(value))}, oczekiwano wartość typu {type_name}.', ctx.start.line)
            else:
                raise ExceptionSPK('Istnieje już zmienna o tej nazwie.', ctx.start.line)

    def exitAssignment(self, ctx: SPKParser.AssignmentContext):  # x = 2;
        if not self.skipping and not self.skipFBlock:
            variable_name = str(ctx.VARIABLE_NAME())
            value = ctx.expr().result
            if self.latest_function_result['name'] == variable_name:
                self.latest_function_result['value'] = value
            else:
                for scope in reversed(self.memory['scopes']):
                    if variable_name in scope.keys():
                        type_name = scope[variable_name]['type']
                        if ctx.list_index():
                            if type_name == 'LISTA':
                                index = ctx.list_index().expr().result
                                if type(index) == int:

                                    variable = scope[variable_name]['value']
                                    if index < len(variable):
                                        variable[index] = value
                                        scope[variable_name]['value'] = variable
                                    else:
                                        raise ExceptionSPK('Indeks listy poza zakresem.', ctx.start.line)
                                        
                                else:
                                    raise ExceptionSPK('Indeks musi być typu całkowitego.', ctx.start.line)

                            else:
                                raise ExceptionSPK('Nie można odnieść się przez indeks do tej zmiennej.', ctx.start.line)
                            
                        else:

                            if correct_type(type_name, value):
                                scope[variable_name]['value'] = value
                            else:
                                raise ExceptionSPK(f'Brak zgodności typów danych w przypisaniu do zmiennej. '
                                                   f'Podano zmienną typu {get_type_SPK(type(value))}, oczekiwano wartość typu {type_name}.', ctx.start.line)

                        return
                raise ExceptionSPK('Nie możesz przypisać wartości do niezainicjowanej zmiennej.', ctx.start.line)

    def enterBlock(self, ctx: SPKParser.BlockContext):
        if self.skipBlock and not self.skipFBlock:
            self.skipping = True
            self.skipExpr = True
        self.memory['scopes'].append({})

    def exitBlock(self, ctx: SPKParser.BlockContext):
        if not self.skipFBlock:
            self.skipping = False
            self.skipExpr = False
            
        self.memory['scopes'].pop(-1)
            # print("Koniec lokalnego scope'a")

    def exitPrint_(self, ctx: SPKParser.Print_Context):
        if not self.skipping and not self.skipFBlock:
            if ctx.expr().result is not None:
                result = ctx.expr().result
                if type(result) == bool:
                    if result:
                        result = 'Prawda'
                    else:
                        result = 'Fałsz'
                print(f"WYPISANIE: {result}")

    def enterFunction_(self, ctx:SPKParser.Function_Context):
        self.skipping = True
        self.skipExpr = True

    def exitFunction_(self, ctx:SPKParser.Function_Context):
        self.skipping = False
        self.skipExpr = False
        
      # Enter a parse tree produced by SPKParser#fblock.
    def enterFblock(self, ctx:SPKParser.FblockContext):
        self.skipFBlock = True

    # Exit a parse tree produced by SPKParser#fblock.
    def exitFblock(self, ctx:SPKParser.FblockContext):
        self.skipFBlock = False

    def enterFunction_exec(self, ctx:SPKParser.Function_execContext):
        if not self.skipping:
            ctx.returned_value = None

    def exitFunction_exec(self, ctx:SPKParser.Function_execContext):
        if not self.skipping and not self.skipFBlock:
            function_name = str(ctx.VARIABLE_NAME())
            if function_name in self.memory['functions'].keys():
                print(f'Wywołanie funkcji {function_name}.')

                f = self.memory['functions'][function_name]

                expected_len = len(f['arguments'])
                actual_len = len(ctx.arguments_exec().expr())
                if expected_len != actual_len:
                    raise ExceptionSPK(f'Nieprawidłowa liczba argumentów. Oczekiwano {expected_len}, otrzymano {actual_len}.', ctx.start.line)

                self.memory['scopes'].append({})

                for arg, arg_exec in zip(f['arguments'], ctx.arguments_exec().expr()):
                    
                    value = arg_exec.result
                    if correct_type(arg['type'], value):
                        self.memory['scopes'][-1][arg['name']] = {'type': arg['type'], 'value': value}
                    else:
                        self.memory['scopes'].pop(-1)
                        raise ExceptionSPK('Niezgodność typów.', ctx.start.line)

                if f['returned']:
                    self.latest_function_result['name'] = f['returned']['name']
                    
                self.walker.walk(self, f['block'])

                if f['returned']:
                    returned_value = self.latest_function_result['value']

                    if correct_type(f['returned']['type'], returned_value):
                        ctx.returned_value = returned_value
                    elif returned_value is None:
                        raise ExceptionSPK(f"Funkcja nie używa zmiennej, którą zwraca.", ctx.start.line)
                    else:
                        raise ExceptionSPK(f"Zmienna zwracana z funkcji jest typu {f['returned']['type']}, a podano typ {get_type_SPK(type(returned_value))}.", ctx.start.line)

                self.memory['scopes'].pop(-1)

            else:
                raise ExceptionSPK(f'Funkcja o nazwie {function_name} nie istnieje.', ctx.start.line)


    def enterExpr(self, ctx:SPKParser.ExprContext):
        ctx.result = None

    def exitExpr(self, ctx:SPKParser.ExprContext):
        operations = {
            'MINUS': {
                (int, int): lambda a, b: a-b,
                (int, float): lambda a, b: a-b,
                (float, int): lambda a, b: a-b,
                (float, float): lambda a, b: a-b
            },
            'PLUS': {
                (int, int): lambda a, b: a+b,
                (int, float): lambda a, b: a+b,
                (float, int): lambda a, b: a+b,
                (float, float): lambda a, b: a+b,
                (str, int): lambda a, b: a+str(b),
                (int, str): lambda a, b: str(a)+b,
                (str, float): lambda a, b: a+str(b),
                (float, str): lambda a, b: str(a)+b,
                (str, str): lambda a, b: a+b,
                (list, list): lambda a, b: a+b
            },
            'MULT': {
                (int, int): lambda a, b: a * b,
                (int, float): lambda a, b: a * b,
                (float, int): lambda a, b: a * b,
                (float, float): lambda a, b: a * b,
                (str, int): lambda a, b: a * b,
                (int, str): lambda a, b: a * b,
                (int, list): lambda a, b: a * b,
                (list, str): lambda a, b: a * b
            },
            'DIV': {
                (int, int): lambda a, b: a / b,
                (int, float): lambda a, b: a / b,
                (float, int): lambda a, b: a / b,
                (float, float): lambda a, b: a / b
            },
            'LTEQ': {
                (int, int): lambda a, b: a <= b,
                (int, float): lambda a, b: a <= b,
                (float, int): lambda a, b: a <= b,
                (float, float): lambda a, b: a <= b,
                (list, list): lambda a, b: a <= b,
                (str, str): lambda a, b: a <= b,
                (bool, bool): lambda a, b: a <= b
            },
            'GTEQ': {
                (int, int): lambda a, b: a >= b,
                (int, float): lambda a, b: a >= b,
                (float, int): lambda a, b: a >= b,
                (float, float): lambda a, b: a >= b,
                (list, list): lambda a, b: a >= b,
                (str, str): lambda a, b: a >= b,
                (bool, bool): lambda a, b: a >= b
            },
            'LT': {
                (int, int): lambda a, b: a < b,
                (int, float): lambda a, b: a < b,
                (float, int): lambda a, b: a < b,
                (float, float): lambda a, b: a < b,
                (list, list): lambda a, b: a < b,
                (str, str): lambda a, b: a < b,
                (bool, bool): lambda a, b: a < b
            },
            'GT': {
                (int, int): lambda a, b: a > b,
                (int, float): lambda a, b: a > b,
                (float, int): lambda a, b: a > b,
                (float, float): lambda a, b: a > b,
                (list, list): lambda a, b: a > b,
                (str, str): lambda a, b: a > b,
                (bool, bool): lambda a, b: a > b
            },
            'EQ': {
                (int, int): lambda a, b: a == b,
                (int, float): lambda a, b: a == b,
                (float, int): lambda a, b: a == b,
                (float, float): lambda a, b: a == b,
                (list, list): lambda a, b: a == b,
                (str, str): lambda a, b: a == b,
                (bool, bool): lambda a, b: a == b
            },
            'NEQ': {
                (int, int): lambda a, b: a != b,
                (int, float): lambda a, b: a != b,
                (float, int): lambda a, b: a != b,
                (float, float): lambda a, b: a != b,
                (list, list): lambda a, b: a != b,
                (str, str): lambda a, b: a != b,
                (bool, bool): lambda a, b: a != b
            }
        }
        if not self.skipFBlock:
            if not self.skipExpr:
                if not ctx.op and ctx.atom():
                    if ctx.atom().LENGTH():
                        value = ctx.atom().expr().result
                        try:
                            ctx.result = len(value)
                        except:
                            raise ExceptionSPK(f'Nie można obliczyć długości zmiennej typu {get_type_SPK(type(value))}.', ctx.start.line)
                        

                        # if ctx.atom().iterable().STRING():
                        #     ctx.result = len(str(ctx.atom().iterable().STRING())[1:-1])
                        # elif ctx.atom().iterable().list_values():
                        #     ctx.result = len(ctx.atom().iterable().list_values().expr())
                        # elif ctx.atom().iterable().VARIABLE_NAME():
                        #     variable_name = str(ctx.atom().iterable().VARIABLE_NAME())
                        #     variable = self.get_variable_value(variable_name, ctx.start.line)
                        #     if type(variable) in (list, str):
                        #         ctx.result = len(variable)
                        #     else:
                        #         raise ExceptionSPK(f'Nie można obliczyć długości zmiennej typu {get_type_SPK(type(variable))}.', ctx.start.line)
                        
                    elif ctx.atom().TO_INT():
                        value = ctx.atom().expr().result
                        try:
                            ctx.result = int(value)
                        except:
                            raise ExceptionSPK(f'JAKO_CAŁKOWITA() oczekuje wartości typu UŁAMKOWA lub NAPIS, podano {get_type_SPK(type(value))}', ctx.start.line)
                        
                    elif ctx.atom().TO_FLOAT():
                        value = ctx.atom().expr().result
                        try:
                            ctx.result = float(value)
                        except:
                            raise ExceptionSPK(f'JAKO_UŁAMKOWA() oczekuje wartości typu CAŁKOWITA lub NAPIS, podano {get_type_SPK(type(value))}', ctx.start.line)
                        
                    elif ctx.atom().TO_STRING():
                        value = ctx.atom().expr().result
                        try:
                            ctx.result = str(value)
                        except:
                            raise ExceptionSPK(f'JAKO_NAPIS() oczekuje wartości typu CAŁKOWITA lub NAPIS, podano {get_type_SPK(type(value))}', ctx.start.line)

                    elif ctx.atom().function_exec():
                        returned_value = ctx.atom().function_exec().returned_value
                        if not returned_value:
                            function_result = self.latest_function_result['value']
                            if function_result is not None:
                                ctx.result = function_result
                            else:
                                raise ExceptionSPK('Ta funkcja nic nie zwraca.', ctx.start.line)
                        else:
                            ctx.result = returned_value
                        #else:
                        #    raise ExceptionSPK('Ta funkcja nic nie zwraca lub zwracana zmienna w funkcji nie została użyta.')

                    elif ctx.atom().VARIABLE_NAME():
                        variable_name = str(ctx.atom().VARIABLE_NAME())
                        if self.latest_function_result['name'] == variable_name:
                            ctx.result = self.latest_function_result['value']
                        else:
                            ctx.result = self.get_variable_value(variable_name, ctx.start.line)

                    elif ctx.atom().INTEGER_NUMBER():
                        ctx.result = int(str(ctx.atom().INTEGER_NUMBER()))
                    elif ctx.atom().FLOAT_NUMBER():
                        ctx.result = float(str(ctx.atom().FLOAT_NUMBER()))
                    elif ctx.atom().STRING():
                        ctx.result = str(ctx.atom().STRING())[1:-1]
                    elif ctx.atom().BOOL_VALUE():
                        ctx.result = True if str(ctx.atom().BOOL_VALUE()) == 'Prawda' else False
                    elif ctx.atom().list_values():
                        ctx.result = [expr.result for expr in ctx.atom().list_values().expr()]
                    elif ctx.atom().list_element():
                        variable = self.get_variable_value(str(ctx.atom().list_element().VARIABLE_NAME()), ctx.start.line)
                        if type(variable) in (str, list):
                            index = ctx.atom().list_element().list_index().expr().result
                            if type(index) == int:
                                ctx.result = variable[index]
                            else:
                                raise ExceptionSPK('Indeks musi być typu całkowitego.', ctx.start.line)

                    elif ctx.atom().range_():
                        start = ctx.atom().range_().expr(0).result
                        end = ctx.atom().range_().expr(1).result
                        if type(start) == type(end) == int:
                            ctx.result = list(range(start, end+1))
                        else:
                            raise ExceptionSPK('[OD .. DO ..] oczekuje typu całkowitego.', ctx.start.line)
                    
                    
                    else:
                        ctx.result = ctx.atom().expr().result

                elif not ctx.op and ctx.MINUS():
                    ctx.result = -1 * ctx.expr(0).result

                elif not ctx.op and ctx.NOT():
                    ctx.result = not ctx.expr(0).result

                elif not ctx.op and ctx.POW() and ctx.expr(0).result is not None and ctx.expr(1).result is not None:
                    
                    try:
                        ctx.result = pow(ctx.expr(0).result, ctx.expr(1).result)
                    except:
                        raise ExceptionSPK(f'Nie można wykonać potęgowania dla typów {get_type_SPK(type(ctx.expr(0).result))} i {get_type_SPK(type(ctx.expr(1).result))}.', ctx.start.line)


                elif ctx.op and ctx.expr(0).result is not None and ctx.expr(1).result is not None:

                    if ctx.MINUS():
                        operation = 'MINUS'
                        # ctx.result = ctx.expr(0).result - ctx.expr(1).result
                    elif ctx.PLUS():
                        operation = 'PLUS'

                        # ctx.result = ctx.expr(0).result + ctx.expr(1).result
                    elif ctx.MULT():
                        operation = 'MULT'

                        # ctx.result = ctx.expr(0).result * ctx.expr(1).result
                    elif ctx.DIV():
                        operation = 'DIV'

                        # ctx.result = ctx.expr(0).result / ctx.expr(1).result
                    elif ctx.LTEQ():
                        operation = 'LTEQ'

                        # ctx.result = ctx.expr(0).result <= ctx.expr(1).result
                    elif ctx.GTEQ():
                        operation = 'GTEQ'

                        # ctx.result = ctx.expr(0).result >= ctx.expr(1).result
                    elif ctx.LT():
                        operation = 'LT'

                        # ctx.result = ctx.expr(0).result < ctx.expr(1).result
                    elif ctx.GT():
                        operation = 'GT'

                        # ctx.result = ctx.expr(0).result > ctx.expr(1).result
                    elif ctx.EQ():
                        operation = 'EQ'

                        # ctx.result = ctx.expr(0).result == ctx.expr(1).result
                    elif ctx.NEQ():
                        operation = 'NEQ'

                        # ctx.result = ctx.expr(0).result != ctx.expr(1).result

                    for types, function in operations[operation].items():
                        if types == (type(ctx.expr(0).result), type(ctx.expr(1).result)):
                            ctx.result = function(ctx.expr(0).result, ctx.expr(1).result)
                            return
                    raise ExceptionSPK(f'Nie można przeprowadzić operacji {operation_in_polish(operation)} na wartościach typu'
                                       f' {get_type_SPK(type(ctx.expr(0).result))} i {get_type_SPK(type(ctx.expr(1).result))}.', ctx.start.line)

                elif ctx.AND():
                    ctx.result = ctx.expr(0).result and ctx.expr(1).result
                elif ctx.OR():
                    ctx.result = ctx.expr(0).result or ctx.expr(1).result
                         
    # Enter a parse tree produced by SPKParser#condition.
    def enterCondition(self, ctx:SPKParser.ConditionContext):
        if not self.skipFBlock:
            self.skipExpr = False
            self.skipping = False
            self.skipBlock = False
            if self.skipCondition:
                self.skipExpr = True

    # Exit a parse tree produced by SPKParser#condition.
    def exitCondition(self, ctx:SPKParser.ConditionContext):
        if not self.skipFBlock:
            self.skipExpr = True
            self.skipping = True
            self.skipBlock = True
            if self.skipCondition:
                self.skipExpr = False

    def enterIf_stat(self, ctx:SPKParser.If_statContext):
        if not self.skipFBlock:
            self.skipExpr = True
            self.skipping = True
            self.skipBlock = True
            self.if_loop_level += 1
        

    # Exit a parse tree produced by SPKParser#if_stat.
    def exitIf_stat(self, ctx:SPKParser.If_statContext):
        if not self.skipFBlock:
            self.skipExpr = False
            self.skipping = False
            self.skipBlock = False
            self.if_loop_level -= 1
            if self.if_loop_level == 0:
                for cond_block in ctx.condition_block():
                    if cond_block.condition().expr().result:
                        self.walker.walk(self, cond_block.block())
                        return
                    
                if ctx.block():
                    self.walker.walk(self, ctx.block())

    def enterWhile_stat(self, ctx):
        if not self.skipFBlock:
            self.while_loop_level += 1
            self.inside_loop = True
            self.skipBlock = True
            self.skipCondition = True

    # Exit a parse tree produced by SPKParser#while_stat.
    def exitWhile_stat(self, ctx:SPKParser.While_statContext):

        if not self.skipFBlock:
            counter = 0
            LIMIT = 1000

            self.while_loop_level -= 1
            self.skipCondition = False
            if self.while_loop_level == 0:

                
                self.skipBlock = False
                while ctx.expr().result:
                    self.walker.walk(self, ctx.block())
                    self.walker.walk(self, ctx.expr())
                    counter+=1
                    if self.break_on:
                        self.skipping = False
                        self.break_on = False
                        break
                    if counter == LIMIT:
                        raise ExceptionSPK('Przekroczono limit rekurencji.', ctx.start.line)
            self.inside_loop = False


            

    # Enter a parse tree produced by SPKParser#for_loop.
    def enterFor_loop(self, ctx:SPKParser.For_loopContext):
        if not self.skipFBlock:
            self.for_loop_level += 1
            self.inside_loop = True
            self.skipBlock = True
            self.skipCondition = True
        
    # Exit a parse tree produced by SPKParser#for_loop.
    def exitFor_loop(self, ctx:SPKParser.For_loopContext):
        if not self.skipFBlock:
            self.for_loop_level -= 1
            self.skipCondition = False
            if self.for_loop_level == 0:

                # self.skipping = False
                self.skipBlock = False

                iterated = None
                if ctx.iterable().VARIABLE_NAME():
                    iterated = self.get_variable_value(str(ctx.iterable().VARIABLE_NAME()), ctx.start.line)
                    if type(iterated) not in (list, str):
                        iterated = None
                elif ctx.iterable().STRING():
                    iterated = str(ctx.iterable().STRING())[1:-1]
                elif ctx.iterable().list_values():
                    iterated = [expr.result for expr in ctx.iterable().list_values().expr()]

                elif ctx.iterable().range_():
                    start = int(ctx.iterable().range_().expr(0).result)
                    end = int(ctx.iterable().range_().expr(1).result)
                    if type(start) == type(end) == int:
                        iterated = list(range(start, end+1))
                    else:
                        raise ExceptionSPK('BŁĄD: [OD .. DO ..] oczekuje typu całkowitego.', ctx.start.line)

                if iterated is not None:
                    for i in iterated:
                        self.memory['scopes'].append({})
                        self.memory['scopes'][-1][str(ctx.VARIABLE_NAME())] = {'type': get_type_SPK(type(i)), 'value': i}
                        self.walker.walk(self, ctx.block())
                        self.memory['scopes'].pop(-1)
                        if self.break_on:
                            self.skipping = False
                            self.break_on = False
                            break

                self.inside_loop = False
                     

            

    # Enter a parse tree produced by SPKParser#break_.
    def enterBreak_(self, ctx:SPKParser.Break_Context):
        if not self.skipping:
            if self.inside_loop:
                self.break_on = True
                self.skipping = True
            else:
                raise ExceptionSPK('Użyto stopu poza pętlą.', ctx.start.line)

   # Enter a parse tree produced by SPKParser#sleep_.
    def exitSleep_(self, ctx:SPKParser.Sleep_Context):
        if not self.skipping:
            t = ctx.expr().result
            if type(t) in (int, float):
                time.sleep(t)
            else:
                raise ExceptionSPK(f'CZEKAJ() oczekuje wartość typu CAŁKOWITA lub UŁAMKOWA, podano {get_type_SPK(type(t))}', ctx.start.line)


    def get_variable_value(self, variable_name, line):
        for scope in reversed(self.memory['scopes']):
            if variable_name in scope.keys():
                value = scope[variable_name]['value']
                return value

        # throw jakiś error
        raise ExceptionSPK(f'Zmienna o nazwie {variable_name} nie istnieje.', line)
        return None



def get_type_SPK(python_type):
    if python_type == int:
        return "CAŁKOWITA"
    elif python_type == float:
        return "UŁAMKOWA"
    elif python_type == str:
        return "NAPIS"
    elif python_type == bool:
        return "LOGICZNA"
    elif python_type == list:
        return "LISTA"
                      
def correct_type(variable_type: str, value):
    if variable_type == 'CAŁKOWITA':
        return type(value) == int
    elif variable_type == 'UŁAMKOWA':
        return type(value) == float
    elif variable_type == 'NAPIS':
        return type(value) == str
    elif variable_type == 'LOGICZNA':
        return type(value) == bool
    elif variable_type == 'LISTA':
        return type(value) == list


def operation_in_polish(operation):
    op_dict = {
        'MINUS': 'ODEJMOWANIE',
        'PLUS': 'DODAWANIE',
        'MULT': 'MNOŻENIE',
        'DIV': 'DZIELENIE',
        'LTEQ': '<=',
        'GTEQ': '>=',
        'LT': '<',
        'GT': '>',
        'EQ': '==',
        'NEQ': '!=',
    }
    return op_dict.get(operation, '')
