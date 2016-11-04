import unittest
from delphiPasParser import *


class OutcomesTest(unittest.TestCase):

    def test_ident(self):
        self.assertTrue(ident.parseString('word').asList()==['word'])
        self.assertTrue(ident.parseString('word asdf').asList()==['word'])


    def test_identList(self):
        self.assertTrue(identList.parseString("list,aabc").asList()==['list','aabc'])
        self.assertTrue(identList.parseString('list aabc').asList()==['list'])


    def test_Particle(self):
        self.assertTrue(Particle.parseString("7").asList()==['7'])
        self.assertTrue(Particle.parseString("word").asList()==['word'])
        self.assertTrue(Particle.parseString("(word)").asList()==['(','word',')'])
        self.assertTrue(Particle.parseString("(word = 3)").asList()==['(', 'word', '=', '3', ')'])
        self.assertTrue(Particle.parseString("[word]").asList()==['[','word',']'])


    def test_Atom(self):
        self.assertTrue(Atom.parseString("word[function.call(word,talking)]").asList()==['word','[','function','.','call','(','word','talking',')',']'])
        self.assertTrue(Atom.parseString("word(function.word(word))").asList()==['word', '(', 'function', '.', 'word', '(', 'word', ')', ')'])
        self.assertTrue(Atom.parseString("""
            MessageDlg('Open Active Query error: ' + id + ' ' + School, mtError, [mbIgnore], 0);
            """).asList()==['MessageDlg', '(', "'Open Active Query error: '", '+', 'id', '+', "' '", 
                '+', 'School', 'mtError', '[', 'mbIgnore', ']', '0', ')'])
        # Atom.parseString("function.word(word2)")
        # Atom.parseString("function(word,worbb)")


    def test_statement(self):
        self.assertTrue(statement.parseString("SQL.Clear").asList()==['SQL','.','Clear'])
        self.assertTrue(statement.parseString("cPeriod:=FieldByName('Time_MP').AsString").asList()==['cPeriod',':=','FieldByName','(',"'Time_MP'",')','.','AsString'])
        self.assertTrue(statement.parseString("cPeriod.FieldByName('Time_MP').AsString;").asList()==['cPeriod','.','FieldByName','(',"'Time_MP'",')','.','AsString'])
        self.assertTrue(statement.parseString("temp := 'WHERE ID_NUMBER =''' + id + ''''").asList()==['temp', ':=', "'WHERE ID_NUMBER ='''", '+', 'id', '+', "''''"])


    def test_expression(self):
        self.assertTrue(expression.parseString("(cPeriod = '')").asList()==['(', 'cPeriod', '=', "''", ')'])
        self.assertTrue(expression.parseString("(cPeriod = '') or (cPeriod = 'N')").asList()==['(', 'cPeriod', '=', "''", ')', 'or', '(', 'cPeriod', '=', "'N'", ')'])
        self.assertTrue(expression.parseString("if expression() then begin end;").asList()==['if'])
        self.assertTrue(expression.parseString("Odin.UseSQL").asList()==['Odin', '.', 'UseSQL'])


    def test_assignment(self):
        self.assertTrue(assignment.parseString('expression.Yourself := NOLA.bounce noParse').asList()==['expression', '.', 'Yourself', ':=', 'NOLA', '.', 'bounce'])
        self.assertTrue(assignment.parseString("ConnectionName := 'OdinSQL'").asList()==['ConnectionName', ':=', "'OdinSQL'"])


    def test_expressionOrAssignment(self):
        self.assertTrue(expressionOrAssignment.parseString("cPeriod := FieldByName('Time_MP').AsString;").asList()==['cPeriod',':=','FieldByName','(',"'Time_MP'",')','.','AsString'])
        self.assertTrue(expressionOrAssignment.parseString("cPeriod.FieldByName('Time_MP').AsString;").asList()==['cPeriod','.','FieldByName','(',"'Time_MP'",')','.','AsString'])


    def test_expressionList(self):
        self.assertTrue(expressionList.parseString('Odin.SumQuery').asList()==['Odin', '.', 'SumQuery'])
        self.assertTrue(expressionList.parseString('Odin.SumQuery do').asList()==['Odin', '.', 'SumQuery'])
        self.assertTrue(expressionList.parseString('True,sortaTrue,MegaTrue.theReal()').asList()==['True','sortaTrue','MegaTrue','.','theReal','(',')'])


    def test_withStatement(self):
        self.assertTrue(withStatement.parseString("""
            with Odin.SumQuery do
            begin
              temp := 'WHERE ID_NUMBER = ''' + id + '''';
              Open;
            end""").asList()==[['with', 'Odin', '.', 'SumQuery', 'do'], 'begin', 'temp', ':=', "'WHERE ID_NUMBER = '''", '+', 'id', '+', "''''", ';', 'Open', ';', 'end'])


    def test_ifStatement(self):
        # pass
        self.assertTrue(ifStatement.parseString("""
            if (cPeriod = '') or (cPeriod = 'N') then
            begin
              sDate := yStart;
              SQL.Add('SELECT DISTINCT LACTIVE');
              ConnectionName := 'OdinSQL';
            end
            """).asList()==['if', '(', 'cPeriod', '=', "''", ')', 'or', '(', 'cPeriod', '=', "'N'", ')', 'then', 'begin', 
        'sDate', ':=', 'yStart', ';', 'SQL', '.', 'Add', '(', "'SELECT DISTINCT LACTIVE'", ')', ';', 'ConnectionName', ':=', "'OdinSQL'", ';', 'end'])

        self.assertTrue(ifStatement.parseString("""
                if Odin.UseSQL then
                begin
                  if (FieldByName('LACTIVE').AsInteger = 1) then
                    result := true
                  else
                    result := false;
                end
            """).asList()==['if', 'Odin', '.', 'UseSQL', 'then', 'begin', 
        'if', '(', 'FieldByName', '(', "'LACTIVE'", ')', '.', 'AsInteger', '=', '1', ')', 'then', 'result', ':=', 'true', 'else', 'result', ':=', 'false', ';', 'end'])

        self.assertTrue(ifStatement.parseString("""
            if (cPeriod = '') or (cPeriod = 'N') then
            begin
              sDate := yStart;
              eDate := Now;
            end
            else if cPeriod = 'T' then
            begin
              sDate := tStart;
              eDate := tEnd;
            end
            """).asList()==['if', '(', 'cPeriod', '=', "''", ')', 'or', '(', 'cPeriod', '=', "'N'", ')', 'then', 
        'begin', 'sDate', ':=', 'yStart', ';', 'eDate', ':=', 'Now', ';', 'end', 'else', 'if', 'cPeriod', '=', "'T'", 'then', 
        'begin', 'sDate', ':=', 'tStart', ';', 'eDate', ':=', 'tEnd', ';', 'end'])


    def test_statementList(self):
        self.assertTrue(statementList.parseString("SQL.Clear;;SQL.Add('SELECT Plan_MP,Time_MP');").asList()==['SQL',
                                                                                '.', 'Clear', ';', ';', 'SQL', '.', 
                                                                                'Add', '(', "'SELECT Plan_MP,Time_MP'", ')', ';'])

        self.assertTrue(statementList.parseString("""
            lTime := CheckTime(start, finish, RegisterCode, plu, location);
            with Odin.SumQuery do
            begin
              if Odin.UseSQL then
              begin
                SQL.Add('FROM meals');
              end
              else
              begin
                SQL.Add('FROM ":Schools:MEALS.DBF"'); 
              end;
              SQL.Add(temp);
            end;
            """).asList()==['lTime', ':=', 'CheckTime', '(', 'start', 'finish', 'RegisterCode', 'plu', 'location', ')', ';', ['with', 'Odin', '.', 'SumQuery', 'do'], 'begin',
                'if', 'Odin', '.', 'UseSQL', 'then', 'begin', 'SQL', '.', 'Add', '(', "'FROM meals'", ')', ';', 'end', 'else', 'begin',
                'SQL', '.', 'Add', '(', '\'FROM ":Schools:MEALS.DBF"\'', ')', ';', 'end', ';', 'SQL', '.', 'Add', '(', 'temp', ')', ';', 'end', ';'])


    def test_block(self):
        self.assertTrue(block.parseString("""
            begin
              begin
              end;
            end
            """).asList()==['begin','begin','end',';','end'])

       #  print(block.parseString("""
       #      begin
       #      result := false;
       #      if Odin.UseSQL or Odin.SQLFields then
       #        ActiveField := 'LACTIVE'
       #      else
       #        ActiveField := 'ACTIVE';

       #      with Odin.LookupQuery do
       #      begin
       #        Close;;
       #        SQL.Clear;
       #        if Odin.UseSQL then
       #        begin
     #          SQL.Add('SELECT DISTINCT LACTIVE');
       #          SQL.Add('FROM student');
       #          ConnectionName := 'OdinSQL';
       #        end
       #        else
       #        begin
       #          SQL.Add('SELECT DISTINCT ":Schools:STUDENT.dbf"."ACTIVE"');
       #          SQL.Add('FROM ":Schools:STUDENT.DBF"');
       #          ConnectionName := 'Schools';
       #        end;
       #        temp := 'WHERE ID_NUMBER = ''' + id + '''';
       #        SQL.Add(temp);
       #        if School > '' then
       #        begin
       #          temp := 'AND SCHOOL = ''' + School + '''';
       #          SQL.Add(temp);
       #        end;
       #        Prepare;
       #        try
       #          Open;
       #        except
       #          MessageDlg('Open Active Query error: ' + id + ' ' + School, mtError,
       #            [mbIgnore], 0);
       #        end;

       #        if Odin.UseSQL or Odin.SQLFields then
       #        begin
       #          if (FieldByName('LACTIVE').AsInteger = 1) then
       #            result := true
       #          else
       #            result := false;
       #        end

       #        else
       #        begin
       #          if FieldByName('ACTIVE').AsBoolean then
       #            result := true;
       #          else
       #            result := false;
       #        end;
       #        Close;
       #      end;
       #    end
       #   """))


    def test_varSection(self):
        self.assertTrue(varSection.parseString("""
            var
              sDate, eDate: TDateTime;
              temp, b: string;
            """).asList()==['var', ['sDate', 'eDate', ':', 'TDateTime', ';'], ['temp', 'b', ':', 'string', ';']])


    def test_parameter(self):
        self.assertTrue(parameter.parseString("const NewEntry: string").asList()==['const', 'NewEntry', ':', 'string'])
        self.assertTrue(parameter.parseString("var NewEntry, OldEntry : string").asList()==['var', 'NewEntry', 'OldEntry', ':', 'string'])


    def test_methodHeading(self):
        self.assertTrue(methodHeading.parseString("function GetMealPlanInfo(var id, cPeriod: string; yStart, eStart: \
            TDateTime): integer;").asList()==['function', 'GetMealPlanInfo', '(', 'var', 'id', 'cPeriod', ':', 'string', ';', 'yStart', 'eStart', ':', 
            'TDateTime', ')', ':', 'integer', ';'])
        self.assertTrue(methodHeading.parseString("procedure SaveFilterStrings(const NewEntry: string);").asList()==['procedure', 'SaveFilterStrings', '(', 'const', 'NewEntry', ':', 'string', ')', ';'])


if __name__ == "__main__":
    unittest.main()