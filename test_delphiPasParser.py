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
        # print(statement.parseString("ItemGrid.Columns[2].FieldName := 'SALE_PRICE'"))


    def test_expression(self):
        self.assertTrue(expression.parseString("(cPeriod = '')").asList()==['(', 'cPeriod', '=', "''", ')'])
        self.assertTrue(expression.parseString("(cPeriod = '') or (cPeriod = 'N')").asList()==['(', 'cPeriod', '=', "''", ')', 'or', '(', 'cPeriod', '=', "'N'", ')'])
        self.assertTrue(expression.parseString("if expression() then begin end;").asList()==['if'])
        self.assertTrue(expression.parseString("Odin.UseSQL").asList()==['Odin', '.', 'UseSQL'])
        self.assertTrue(expression.parseString("2").asList()==['2'])
        self.assertTrue(expression.parseString("""FieldByName('DeptMarkup').AsFloat >= 0""").asList()==['FieldByName', '(', "'DeptMarkup'", ')', '.', 'AsFloat', '>=', '0'])


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


    # def test_statement(self):
    #     print(statement.parseString("""temp := FieldByName('Unit_Cost').AsFloat * 
    #     (1 + FieldByName('DeptMarkup').AsFloat)"""))


    def test_withStatement(self):
        self.assertTrue(withStatement.parseString("""
            with Odin.SumQuery do
            begin
              temp := 'WHERE ID_NUMBER = ''' + id + '''';
              Open;
            end""").asList()==['with', 'Odin', '.', 'SumQuery', 'do', 'begin', 'temp', ':=', "'WHERE ID_NUMBER = '''", '+', 'id', '+', "''''", ';', 'Open', ';', 'end'])
        # print(withStatement.parseString("""
        #               with DataSet do
        #       begin
        #         if FieldByName('DeptMarkup').AsFloat >= 0 then
        #           temp := FieldByName('Unit_Cost').AsFloat * 
        #             (1 + FieldByName('DeptMarkup').AsFloat)
        #         else
        #           temp := FieldByName('Retail').AsFloat * 
        #             (1 + FieldByName('DeptMarkup').AsFloat);
        #         FieldByName('DeptPrice').AsFloat := RoundUp(temp);
        #       end;""")) # Passes


    def test_ifStatement(self):
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
        # print(ifStatement.parseString("""if FieldByName('DeptMarkup').AsFloat >= 0 then
        #     temp := FieldByName('Unit_Cost').AsFloat * 
        #         (1 + FieldByName('DeptMarkup').AsFloat)
        #     else
        #     temp := FieldByName('Retail').AsFloat * 
        #         (1 + FieldByName('DeptMarkup').AsFloat);""")) # Passes


    # def test_tryStatement(self):
        # print(tryStatement.parseString("""try
        #     OdinSQL.Connected := True;
        #     except
        #     ODBCConnectError;
        #     end""")) # Passes
        # print(tryStatement.parseString("""try
        #     if SysReg.KeyExists(a) then
        #     begin
        #       SysReg.OpenKey(a, true);
        #       temp := SysReg.ReadString('Server');
        #       if temp <> server then
        #       begin
        #         SysReg.WriteString('Server', server);
        #       end;
        #     end;
        #   finally
        #     SysReg.Free;
        #   end;""")) # Passes


    def test_caseStatement(self):
        self.assertTrue(caseStatement.parseString("""case Key of
    VK_RETURN:
      PreUpdateList(nQty, false);
  else
  end;""").asList()==['case', 'Key', 'of', 'VK_RETURN', ':', 'PreUpdateList', '(', 'nQty', 'false', ')', ';', 'else', 'end'])


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
            """).asList()==['lTime', ':=', 'CheckTime', '(', 'start', 'finish', 'RegisterCode', 'plu', 'location', ')', ';', 'with', 'Odin', '.', 'SumQuery', 'do', 'begin',
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


#     def test_fancyBlock(self):
#         print(fancyBlock.parseString("begin Animate.Active := false; SplashTimer.Enabled := false; end"))
#         print(fancyBlock.parseString("""var
#   response: word;
#   id: string;
# begin
#   CreateLog(GetShared + '\Error.log', True);
#   WriteMessage('Table edit error ' + DataSet.Name + ' ' + E.Message);
#   if DataSet.Name = 'StudentTable' then
#   begin
#     id := DataSet.FieldByName('ID_Number').AsString;
#     WriteMessage('Error editing Id ' + id);
#   end;
#   CloseLog(True);
#   response := MessageDlg('Unable to Edit' + CR + LF + DataSet.Name + CR + LF +
#     E.Message + '     ', mtError, [mbCancel, mbRetry], 0);

#   if response = mrRetry then
#     Action := daRetry
#   else
#     Action := daAbort;
# end""")) # Passes


    def test_varSection(self):
        self.assertTrue(varSection.parseString("""
            var
              sDate, eDate: TDateTime;
              temp, b: string;
            """).asList()==['var', ['sDate', 'eDate', ':', 'TDateTime', ';'], ['temp', 'b', ':', 'string', ';']])
        self.assertTrue(varSection.parseString("""var
  DateTo, DateFrom: TDateTime;
  nBooks: array of TBookmark;""").asList()==['var', ['DateTo', 'DateFrom', ':', 'TDateTime', ';'], ['nBooks', ':', 'array', 'of', 'TBookmark', ';']])


    def test_parameter(self):
        self.assertTrue(parameter.parseString("const NewEntry: string").asList()==['const', 'NewEntry', ':', 'string'])
        self.assertTrue(parameter.parseString("var NewEntry, OldEntry : string").asList()==['var', 'NewEntry', 'OldEntry', ':', 'string'])


    def test_parameterType(self):
        self.assertTrue(parameterType.parseString("array of TBookmark; ").asList()==['array', 'of', 'TBookmark'])


    def test_methodHeading(self):
        self.assertTrue(methodHeading.parseString("procedure ODBCConnectError;").asList()==['procedure', 'ODBCConnectError', ';'])
        self.assertTrue(methodHeading.parseString("function GetMealPlanInfo(var id, cPeriod: string; yStart, eStart: \
            TDateTime): integer;").asList()==['function', 'GetMealPlanInfo', '(', 'var', 'id', 'cPeriod', ':', 'string', ';', 'yStart', 'eStart', ':', 
            'TDateTime', ')', ':', 'integer', ';'])
        self.assertTrue(methodHeading.parseString("procedure SaveFilterStrings(const NewEntry: string);").asList()==['procedure', 'SaveFilterStrings', '(', 'const', 'NewEntry', ':', 'string', ')', ';'])
        self.assertTrue(methodHeading.parseString("""procedure TableEditError(DataSet: TDataSet; E: EDatabaseError;
      var Action: TDataAction);""").asList()==['procedure', 'TableEditError', '(', 'DataSet', ':', 'TDataSet', ';', 'E', ':', 'EDatabaseError', ';', 'var', 'Action', ':', 'TDataAction', ')', ';'])
        self.assertTrue(methodHeading.parseString("""procedure TOdin.SchoolsCreate(Sender: TObject);begin end;""").asList()==['procedure', 'TOdin', '.', 'SchoolsCreate', '(', 'Sender', ':', 'TObject', ')', ';'])
        self.assertTrue(methodHeading.parseString("""function NewWindowProc(WindowHandle: hWnd; TheMessage: LongInt; 
            ParamW: LongInt; ParamL: LongInt): LongInt stdcall;""").asList()==['function', 'NewWindowProc', '(', 'WindowHandle', ':', 'hWnd', ';', 'TheMessage', ':', 'LongInt', ';', 
        'ParamW', ':', 'LongInt', ';', 'ParamL', ':', 'LongInt', ')', ':', 'LongInt', 'stdcall', ';'])
        self.assertTrue(methodHeading.parseString("function OpenUSBcr: integer; stdcall; external 'usbcr.dll';").asList()==['function', 'OpenUSBcr', ':', 'integer', ';', 'stdcall', ';', 'external', 'usbcr.dll', ';'])


    def test_methodImplementation(self):
        self.assertTrue(methodImplementation.parseString("""procedure TSplashForm.FormClose(Sender: TObject; var Action: TCloseAction);
begin
Animate.Active := false;
SplashTimer.Enabled := false;
end;""").asList()==['procedure', 'TSplashForm', '.', 'FormClose', '(', 'Sender', ':', 'TObject', ';', 'var', 'Action', ':', 'TCloseAction', ')', ';', 
        'begin', 'Animate', '.', 'Active', ':=', 'false', ';', 'SplashTimer', '.', 'Enabled', ':=', 'false', ';', 'end', ';'])
        self.assertTrue(methodImplementation.parseString("""procedure TOdin.ODBCConnectError;
var
  response: word;
begin
  CreateLog(GetShared + '\Error.log', True);
  if RetryCount <= 3 then
  begin
    if not OdinSQL.Connected then
    begin
      WriteMessage('SQL reconnect');
      OdinSQL.Connected := True;
    end;
  end
  else
  begin
    response := MessageDlg('Unable to connect to ODBC  ', mtError,
      [mbCancel, mbRetry], 0);
  end;
end;""").asList()==['procedure', 'TOdin', '.', 'ODBCConnectError', ';', 'var', ['response', ':', 'word', ';'], 'begin', 'CreateLog', '(', 'GetShared', '+', "'\\Error.log'", 'True', ')', ';', 
'if', 'RetryCount', '<=', '3', 'then', 'begin', 'if', 'not', 'OdinSQL', '.', 'Connected', 'then', 'begin', 'WriteMessage', '(', "'SQL reconnect'", ')', ';', 
'OdinSQL', '.', 'Connected', ':=', 'True', ';', 'end', ';', 'end', 'else', 'begin', 'response', ':=', 'MessageDlg', '(', "'Unable to connect to ODBC  '", 'mtError', '[', 'mbCancel', 'mbRetry', ']', 
'0', ')', ';', 'end', ';', 'end', ';'])
#         print(methodImplementation.parseString("""procedure TOdin.InitializeSchools;
# var
#   List: TStringList;
#   NewPath, DriverName, cAlias: string;
#   Driver: integer;
#   lSQLAction, lSQLInventry, lSQLtuition, lSQLvendor: boolean;
#   aUser, bUser, pw: string;
# begin
#   SQLFields := False;
#   lSQLAction := False;
#   lSQLInventry := False;
#   lSQLvendor := False;
#   lSQLdb := False;
#   lSQLtuition := False;
#   GetHomeDirectory(HomeDirectory);

#   SchoolsSession.PrivateDir := HomeDirectory;
#   SchoolsSession.NetFileDir := HomeDirectory;

#   SchoolsSession.Active := True;
#   if not SchoolsSession.IsAlias('Schools') then
#   begin
#     ShowMessage('Alias Schools does not exist');
#     Application.Terminate;
#   end;

#   Schools.Close;

#   cAlias := Schools.AliasName;
#   SchoolsSession.GetAliasParams(cAlias, Schools.Params);

#   if FindCmdLineSwitch('path', ['/', '-'], True) then
#   begin
#     NewPath := GetCmdLinePath;
#     bdeDir := NewPath + '\';
#   end
#   else
#     bdeDir := Schools.Params.Values['Path'] + '\';

#   if FindCmdLineSwitch('archive', ['/', '-'], True) then
#   begin
#     Schools.ReadOnly := True;
#     TransactTable.ReadOnly := True;
#     TransferTable.ReadOnly := True;
#     StoreTable.ReadOnly := True;
#     InventoryTable.ReadOnly := True;
#     StudentTable.ReadOnly := True;
#   end;

#   Driver := GetDriver(DriverName, dbReference, lFullSQL, WebStock, lRef_dbo,
#     ServerType);
#   if CheckSQL('Action') then
#     lSQLAction := True;
#   if CheckSQL('db') then
#     lSQLdb := True;
#   if CheckSQL('Inventry') then
#     lSQLInventry := True;
#   if CheckSQL('Vendor') then
#     lSQLvendor := True;
#   if CheckSQL('Tuition') then
#     lSQLtuition := True;

#   LocalTranTable.TableName := HomeDirectory + '\LoclTran.dbf';
#   LocalTransfersTable.TableName := HomeDirectory + '\LoclTransfers.dbf';
#   BankBatchTable.TableName := HomeDirectory + '\BankBatch.dbf';
#   LocalRemotesTable.TableName := HomeDirectory + '\LoclRemotes.dbf';
#   TemptranTable.TableName := HomeDirectory + '\Temptran.dbf';
#   LocalWebTransfers.TableName := HomeDirectory + '\LocalWebTransfers.dbf';

#   if NewPath > '' then
#   begin
#     Schools.Params.Values['Path'] := NewPath;
#     if FindCmdLineSwitch('debug', ['/', '-'], True) then
#       ShowMessage('Switching path to ' + NewPath);
#   end;

#   if SchoolsSession.IsAlias('OdinSQL') then
#   begin
#     Schools.Open;
#     with Odin do
#     begin
#       TranQuerySQL.DatabaseName := 'OdinSQL';
#       TransactTable.DatabaseName := 'OdinSQL';
#       TransactTable.TableType := ttDefault;
#       TransactTable.TableName := 'Transact';

#       TransferQuery.DatabaseName := 'OdinSQL';
#       TransferTable.DatabaseName := 'OdinSQL';
#       TransferTable.TableType := ttDefault;
#       TransferTable.TableName := 'Transfer';

#       StudQuerySQL.DatabaseName := 'OdinSQL';
#       StudentTable.DatabaseName := 'OdinSQL';
#       StudentTable.TableType := ttDefault;
#       StudentTable.TableName := 'Student';

#       CustomRestrictTable.DatabaseName := 'OdinSQL';
#       CustomRestrictTable.TableType := ttDefault;
#       CustomRestrictTable.TableName := 'cstmrsct';

#       if lSQLAction then
#       begin
#         ActionQuery.DatabaseName := 'OdinSQL';
#         ActionTable.DatabaseName := 'OdinSQL';
#         ActionTable.TableType := ttDefault;
#         ActionTable.TableName := 'Action';
#         LostQuery.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLInventry then
#       begin
#         InventoryTable.DatabaseName := 'OdinSQL';
#         InventoryTable.TableType := ttDefault;
#         InventoryTable.TableName := 'inventry';
#         InvQuerySQL.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLvendor then
#       begin
#         VendorTable.DatabaseName := 'OdinSQL';
#         VendorTable.TableType := ttDefault;
#         VendorTable.TableName := 'vendor';
#         VendorSQL.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLtuition then
#       begin
#         TuitionTable.DatabaseName := 'OdinSQL';
#         TuitionTable.TableName := 'tuition';
#         TuitionTable.TableType := ttDefault;
#         TuitionSetupTable.DatabaseName := 'OdinSQL';
#         TuitionSetupTable.IndexName := 'class';
#         TuitionSetupTable.TableName := 'tuitionsetup';
#         TuitionSetupTable.TableType := ttDefault;
#         TuitionPlansTable.DatabaseName := 'OdinSQL';
#         TuitionPlansTable.TableName := 'tuitnpayplan';
#         TuitionPlansTable.TableType := ttDefault;
#         TuitnPayTable.DatabaseName := 'OdinSQL';
#         TuitnPayTable.TableName := 'tuitnpay';
#         TuitnPayTable.TableType := ttDefault;
#         TuitnPaySQL.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLdb then
#       begin
#         RightsTable.TableType := ttDefault;
#         RightsTable.DatabaseName := 'OdinSQL';
#         RightsTable.TableName := 'rights';
#         UsersTable.TableType := ttDefault;
#         UsersTable.DatabaseName := 'OdinSQL';
#         UsersTable.TableName := 'users';
#         WebtranTable.TableType := ttDefault;
#         WebtranTable.DatabaseName := 'OdinSQL';
#         WebtranTable.TableName := 'webtran';
#       end;

#       OdinSQL.Connected := True;
#       UseSQL := True;

#       UseDBX := False;
#       UseODBC := False;
#     end;
#   end

#   else if Driver = ODBC then
#   begin
#     OdinSQL.AliasName := DriverName;
#     Schools.Open;
#     TranQuerySQL.DatabaseName := 'OdinSQL';
#     TransactTable.DatabaseName := 'OdinSQL';
#     TransactTable.TableType := ttDefault;
#     if dbReference > '' then
#       TransactTable.TableName := dbReference + '.transact'
#     else
#       TransactTable.TableName := 'transact';

#     TransferQuery.DatabaseName := 'OdinSQL';
#     TransferTable.DatabaseName := 'OdinSQL';
#     TransferTable.TableType := ttDefault;
#     if dbReference > '' then
#       TransferTable.TableName := dbReference + '.transfer'
#     else
#       TransferTable.TableName := 'transfer';

#     StudQuerySQL.DatabaseName := 'OdinSQL';
#     StudLookupSQL.DatabaseName := 'OdinSQL';
#     StudentTable.DatabaseName := 'OdinSQL';
#     StudentTable.TableType := ttDefault;

#     CustomRestrictTable.DatabaseName := 'OdinSQL';
#     CustomRestrictTable.TableType := ttDefault;
#     CustomRestrictTable.TableName := 'cstmrsct';

#     if lSQLAction then
#     begin
#       ActionQuery.DatabaseName := 'OdinSQL';
#       ActionTable.DatabaseName := 'OdinSQL';
#       ActionTable.TableType := ttDefault;
#       ActionTable.TableName := 'action';
#       LostQuery.DatabaseName := 'OdinSQL';
#     end;

#     if lSQLInventry then
#     begin
#       InventoryTable.DatabaseName := 'OdinSQL';
#       InventoryTable.TableType := ttDefault;
#       InventoryTable.TableName := 'inventry';
#       InvQuerySQL.DatabaseName := 'OdinSQL';
#     end;

#     if lSQLvendor then
#     begin
#       VendorTable.DatabaseName := 'OdinSQL';
#       VendorTable.TableType := ttDefault;
#       VendorTable.TableName := 'vendor';
#       VendorSQL.DatabaseName := 'OdinSQL';
#     end;
#     if lSQLtuition then
#     begin
#       TuitionTable.DatabaseName := 'OdinSQL';
#       TuitionTable.TableName := 'tuition';
#       TuitionTable.TableType := ttDefault;
#       TuitionSetupTable.DatabaseName := 'OdinSQL';
#       TuitionSetupTable.TableName := 'tuitionsetup';
#       TuitionSetupTable.TableType := ttDefault;
#       TuitionSetupTable.IndexName := 'class';
#       TuitionPlansTable.DatabaseName := 'OdinSQL';
#       TuitionPlansTable.TableName := 'tuitnpayplan';
#       TuitionPlansTable.TableType := ttDefault;
#       TuitnPayTable.DatabaseName := 'OdinSQL';
#       TuitnPayTable.TableName := 'tuitnpay';
#       TuitnPayTable.TableType := ttDefault;
#       TuitnPaySQL.DatabaseName := 'OdinSQL';
#     end;

#     if lSQLdb then
#     begin
#       RightsTable.TableType := ttDefault;
#       RightsTable.DatabaseName := 'OdinSQL';
#       RightsTable.TableName := 'rights';
#       UsersTable.TableType := ttDefault;
#       UsersTable.DatabaseName := 'OdinSQL';
#       UsersTable.TableName := 'users';
#       WebtranTable.TableType := ttDefault;
#       WebtranTable.DatabaseName := 'OdinSQL';
#       WebtranTable.TableName := 'webtran';
#     end;

#     if dbReference > '' then
#       StudentTable.TableName := dbReference + '.student'
#     else if (ServerType = stMS2005) and not lRef_dbo then
#       StudentTable.TableName := 'student'
#     else if (ServerType = stMS2005) then
#       StudentTable.TableName := 'dbo.student'
#     else
#       StudentTable.TableName := 'student';
#     Students.DataSet := StudentTable;

#     try
#       OdinSQL.Connected := True;
#     except
#       ODBCConnectError;
#     end;
#     UseODBC := True;
#     UseSQL := True;
#     UseDBX := False;
#   end

#   else if Driver = DBX then
#   begin
#     OdinSQL.AliasName := 'MyKidsODBC';
#     Schools.Open;
#   end

#   else
#   begin
#     if NewPath > '' then
#     begin
#       Schools.Params.Values['Path'] := NewPath;
#     end;

#     TranQuerySQL.DatabaseName := 'Schools';
#     TransactTable.DatabaseName := 'Schools';
#     TransactTable.TableType := ttDBase;
#     TransactTable.TableName := 'Transact.dbf';

#     TransferQuery.DatabaseName := 'Schools';
#     TransferTable.DatabaseName := 'Schools';
#     TransferTable.TableType := ttDBase;
#     TransferTable.TableName := 'Transfer.dbf';

#     StudQuerySQL.DatabaseName := 'Schools';
#     StudentTable.DatabaseName := 'Schools';
#     StudentTable.TableType := ttDBase;
#     StudentTable.TableName := 'Student.dbf';
#     Students.DataSet := StudentTable;

#     UseSQL := False;
#     UseDBX := False;

#     Schools.Open;
#   end;

#   Schools.Connected := True;
#   SchoolsSession.NetFileDir := bdeDir;
# end;"""))


    def test_usesClause(self):
        self.assertTrue(usesClause.parseString("uses Windows, Messages, FireDAC.DApt.Intf, FireDAC.Comp.Client; // , DbxDevartMySql;").asList()==['uses', 'Windows', 'Messages', 'FireDAC', '.', 'DApt', '.', 'Intf', 'FireDAC', '.', 'Comp', '.', 'Client', ';'])
        self.assertTrue(usesClause.parseString("""uses
            Windows, Db, FireDAC.DApt.Intf, FireDAC.Comp.Client; // , DbxDevartMySql;

            type
              TOdin = class(TDataModule)""").asList()==['uses', 'Windows', 'Db', 'FireDAC', '.', 'DApt', '.', 'Intf', 'FireDAC', '.', 'Comp', '.', 'Client', ';'])


    def test_fieldDecl(self):
        self.assertTrue(fieldDecl.parseString("Addresses: TDataSource;").asList()==['Addresses', ':', 'TDataSource', ';'])
        self.assertTrue(fieldDecl.parseString("""Addresses: TDataSource; 
            procedure OdinSQLLogin(Database: TDatabase; LoginParams: TStrings);""").asList()==['Addresses', ':', 'TDataSource', ';'])


    # def test_fieldSection(self):
    #     pass


  #   def test_visibilitySection(self):
  #       print(visibilitySection.parseString("""Schools: TDatabase;
  #   Addresses: TDataSource;
  #   procedure OdinSQLLogin(Database: TDatabase; LoginParams: TStrings);   # This stops at the 'private' decl but I believe that's correct
  #   procedure ODBCConnectError;                                           # and a better test of this sample code is below, under classType
  # private
  #   RetryCount: integer;
  # public
  #   LocalStock: TTable;"""))


    def test_classType(self):
        self.assertTrue(classType.parseString("""class(TDataModule)
    Schools: TDatabase;
    Addresses: TDataSource;
    procedure OdinSQLLogin(Database: TDatabase; LoginParams: TStrings);
    procedure ODBCConnectError;
  private
    RetryCount: integer;
  public
    LocalStock: TTable; end""").asList()==[['class', '(', 'TDataModule', ')', 'Schools', ':', 'TDatabase', ';', 'Addresses', ':', 'TDataSource', ';', 
        'procedure', 'OdinSQLLogin', '(', 'Database', ':', 'TDatabase', ';', 'LoginParams', ':', 'TStrings', ')', ';', 'procedure', 'ODBCConnectError', ';', 
        'private', 'RetryCount', ':', 'integer', ';', 'public', 'LocalStock', ':', 'TTable', ';', 'end']])


    def test_arrayType(self):
        self.assertTrue(arrayType.parseString("array of TBookmark;").asList()==['array', 'of', 'TBookmark'])


    def test__type(self):
        self.assertTrue(classType.parseString("""class(TDataModule)
    Schools: TDatabase;
    Addresses: TDataSource;
    procedure OdinSQLLogin(Database: TDatabase; LoginParams: TStrings);
    procedure ODBCConnectError;
  private
    RetryCount: integer;
  public
    LocalStock: TTable; end""").asList()==[['class', '(', 'TDataModule', ')', 'Schools', ':', 'TDatabase', ';', 'Addresses', ':', 'TDataSource', ';', 'procedure', 
    'OdinSQLLogin', '(', 'Database', ':', 'TDatabase', ';', 'LoginParams', ':', 'TStrings', ')', ';', 'procedure', 'ODBCConnectError', ';', 'private', 
    'RetryCount', ':', 'integer', ';', 'public', 'LocalStock', ':', 'TTable', ';', 'end']])


    def test_typeDecl(self):
        self.assertTrue(typeDecl.parseString("""TOdin = class(TDataModule)
    Schools: TDatabase;
    procedure OdinSQLLogin(Database: TDatabase; LoginParams: TStrings);
    procedure ODBCConnectError;
  private
    RetryCount: integer;
  public
    LocalStock: TTable;
   end;""").asList()==['TOdin', '=', ['class', '(', 'TDataModule', ')', 'Schools', ':', 'TDatabase', ';', 'procedure', 'OdinSQLLogin', '(', 'Database', ':', 'TDatabase', ';', 
        'LoginParams', ':', 'TStrings', ')', ';', 'procedure', 'ODBCConnectError', ';', 'private', 'RetryCount', ':', 'integer', ';', 'public', 'LocalStock', ':', 'TTable', ';', 'end'], ';'])


    def test_typeSection(self):
        self.assertTrue(typeSection.parseString("""type
  TOdin = class(TDataModule)
    Schools: TDatabase;
    procedure OdinSQLLogin(Database: TDatabase; LoginParams: TStrings);
    procedure ODBCConnectError;
  private
    RetryCount: integer;
  public
    LocalStock: TTable;
   end;
""").asList()==['type', 'TOdin', '=', ['class', '(', 'TDataModule', ')', 'Schools', ':', 'TDatabase', ';', 'procedure', 'OdinSQLLogin', '(', 'Database', ':', 'TDatabase', ';', 
        'LoginParams', ':', 'TStrings', ')', ';', 'procedure', 'ODBCConnectError', ';', 'private', 'RetryCount', ':', 'integer', ';', 'public', 'LocalStock', ':', 'TTable', ';', 'end'], ';'])


    def test_constSection(self):
        self.assertTrue(constSection.parseString("""const
  stMS2005 = 2;""").asList()==['const', 'stMS2005', '=', '2', ';'])
        self.assertTrue(constSection.parseString("""const
  stUnknown = 0;
  stMySQL = 1;""").asList()==['const', 'stUnknown', '=', '0', ';', 'stMySQL', '=', '1', ';'])


    def test_interfaceDecl(self):
        self.assertTrue(interfaceDecl.parseString("""type
  TOdin = class(TDataModule)
    Schools: TDatabase;
    procedure OdinSQLLogin(Database: TDatabase; LoginParams: TStrings);
    procedure ODBCConnectError;
  private
    RetryCount: integer;
  public
    LocalStock: TTable;
   end;
""").asList()==['type', 'TOdin', '=', ['class', '(', 'TDataModule', ')', 'Schools', ':', 'TDatabase', ';', 'procedure', 'OdinSQLLogin', '(', 'Database', ':', 'TDatabase', ';', 
        'LoginParams', ':', 'TStrings', ')', ';', 'procedure', 'ODBCConnectError', ';', 'private', 'RetryCount', ':', 'integer', ';', 'public', 'LocalStock', ':', 'TTable', ';', 'end'], ';'])


    # def test_interfaceSection(self):
    #     print(interfaceSection.parseString("""""")) # Fails

    
    # def test_implementationDecl(self):
    #     print(implementationDecl.parseString(""""""))


#     def test_implementationSection(self):
#         print(implementationSection.parseString("""implementation

# uses SharedFunction, SharedConfig;

# procedure TOdin.StoreTableCalcFields(DataSet: TDataSet);
# var
#   temp: currency;
# begin
#   with DataSet do
#   begin
#     if FieldByName('DeptMarkup').AsFloat >= 0 then
#       temp := FieldByName('Unit_Cost').AsFloat *
#         (1 + FieldByName('DeptMarkup').AsFloat)
#     else
#       temp := FieldByName('Retail').AsFloat *
#         (1 + FieldByName('DeptMarkup').AsFloat);
#     FieldByName('DeptPrice').AsFloat := RoundUp(temp);
#   end;

# end;

# procedure TOdin.SchoolsCreate(Sender: TObject);
# begin
#   InitializeSchools;
# end;

# procedure TOdin.InitializeSchools;
# var
#   List: TStringList;
#   NewPath, DriverName, cAlias: string;
#   Driver: integer;
#   lSQLAction, lSQLInventry, lSQLtuition, lSQLvendor: boolean;
#   aUser, bUser, pw: string;
# begin

#   SQLFields := False;
#   lSQLAction := False;
#   lSQLInventry := False;
#   lSQLvendor := False;
#   lSQLdb := False;
#   lSQLtuition := False;

#   GetHomeDirectory(HomeDirectory);

#   SchoolsSession.PrivateDir := HomeDirectory;
#   SchoolsSession.NetFileDir := HomeDirectory

#   SchoolsSession.Active := True;
#   if not SchoolsSession.IsAlias('Schools') then
#   begin
#     ShowMessage('Alias Schools does not exist');
#     Application.Terminate;
#   end;

#   Schools.Close;
#   cAlias := Schools.AliasName;
#   SchoolsSession.GetAliasParams(cAlias, Schools.Params);

#   if FindCmdLineSwitch('path', ['/', '-'], True) then
#   begin
#     NewPath := GetCmdLinePath;
#     bdeDir := NewPath + '\';
#   end
#   else
#     bdeDir := Schools.Params.Values['Path'] + '\';


#   if FindCmdLineSwitch('archive', ['/', '-'], True) then
#   begin
#     Schools.ReadOnly := True;
#     TransactTable.ReadOnly := True;
#     TransferTable.ReadOnly := True;
#     StoreTable.ReadOnly := True;
#     InventoryTable.ReadOnly := True;
#     StudentTable.ReadOnly := True;
#   end;

#   Driver := GetDriver(DriverName, dbReference, lFullSQL, WebStock, lRef_dbo,
#     ServerType);
#   if CheckSQL('Action') then
#     lSQLAction := True;
#   if CheckSQL('db') then
#     lSQLdb := True;
#   if CheckSQL('Inventry') then
#     lSQLInventry := True;
#   if CheckSQL('Vendor') then
#     lSQLvendor := True;
#   if CheckSQL('Tuition') then
#     lSQLtuition := True;

#   LocalTranTable.TableName := HomeDirectory + '\LoclTran.dbf';
#   LocalTransfersTable.TableName := HomeDirectory + '\LoclTransfers.dbf';
#   BankBatchTable.TableName := HomeDirectory + '\BankBatch.dbf';
#   LocalRemotesTable.TableName := HomeDirectory + '\LoclRemotes.dbf';
#   TemptranTable.TableName := HomeDirectory + '\Temptran.dbf';
#   LocalWebTransfers.TableName := HomeDirectory + '\LocalWebTransfers.dbf';

#   if NewPath > '' then
#   begin
#     Schools.Params.Values['Path'] := NewPath;
#     if FindCmdLineSwitch('debug', ['/', '-'], True) then
#       ShowMessage('Switching path to ' + NewPath);
#   end;

#   if SchoolsSession.IsAlias('OdinSQL') then
#   begin
#     Schools.Open;
#     with Odin do
#     begin
#       TranQuerySQL.DatabaseName := 'OdinSQL';
#       TransactTable.DatabaseName := 'OdinSQL';
#       TransactTable.TableType := ttDefault;
#       TransactTable.TableName := 'Transact';

#       TransferQuery.DatabaseName := 'OdinSQL';
#       TransferTable.DatabaseName := 'OdinSQL';
#       TransferTable.TableType := ttDefault;
#       TransferTable.TableName := 'Transfer';

#       StudQuerySQL.DatabaseName := 'OdinSQL';
#       StudentTable.DatabaseName := 'OdinSQL';
#       StudentTable.TableType := ttDefault;
#       StudentTable.TableName := 'Student';

#       CustomRestrictTable.DatabaseName := 'OdinSQL';
#       CustomRestrictTable.TableType := ttDefault;
#       CustomRestrictTable.TableName := 'cstmrsct';

#       if lSQLAction then
#       begin
#         ActionQuery.DatabaseName := 'OdinSQL';
#         ActionTable.DatabaseName := 'OdinSQL';
#         ActionTable.TableType := ttDefault;
#         ActionTable.TableName := 'Action';
#         LostQuery.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLInventry then
#       begin
#         InventoryTable.DatabaseName := 'OdinSQL';
#         InventoryTable.TableType := ttDefault;
#         InventoryTable.TableName := 'inventry';
#         InvQuerySQL.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLvendor then
#       begin
#         VendorTable.DatabaseName := 'OdinSQL';
#         VendorTable.TableType := ttDefault;
#         VendorTable.TableName := 'vendor';
#         VendorSQL.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLtuition then
#       begin
#         TuitionTable.DatabaseName := 'OdinSQL';
#         TuitionTable.TableName := 'tuition';
#         TuitionTable.TableType := ttDefault;
#         TuitionSetupTable.DatabaseName := 'OdinSQL';
#         TuitionSetupTable.IndexName := 'class';
#         TuitionSetupTable.TableName := 'tuitionsetup';
#         TuitionSetupTable.TableType := ttDefault;
#         TuitionPlansTable.DatabaseName := 'OdinSQL';
#         TuitionPlansTable.TableName := 'tuitnpayplan';
#         TuitionPlansTable.TableType := ttDefault;
#         TuitnPayTable.DatabaseName := 'OdinSQL';
#         TuitnPayTable.TableName := 'tuitnpay';
#         TuitnPayTable.TableType := ttDefault;
#         TuitnPaySQL.DatabaseName := 'OdinSQL';
#       end;

#       if lSQLdb then
#       begin
#         RightsTable.TableType := ttDefault;
#         RightsTable.DatabaseName := 'OdinSQL';
#         RightsTable.TableName := 'rights';
#         UsersTable.TableType := ttDefault;
#         UsersTable.DatabaseName := 'OdinSQL';
#         UsersTable.TableName := 'users';
#         WebtranTable.TableType := ttDefault;
#         WebtranTable.DatabaseName := 'OdinSQL';
#         WebtranTable.TableName := 'webtran';
#       end;

#       OdinSQL.Connected := True;
#       UseSQL := True;

#       UseDBX := False;
#       UseODBC := False;
#     end;
#   end

#   else if Driver = ODBC then
#   begin
#     OdinSQL.AliasName := DriverName;
#     Schools.Open;
#     TranQuerySQL.DatabaseName := 'OdinSQL';
#     TransactTable.DatabaseName := 'OdinSQL';
#     TransactTable.TableType := ttDefault;
#     if dbReference > '' then
#       TransactTable.TableName := dbReference + '.transact'
#     else
#       TransactTable.TableName := 'transact';

#     TransferQuery.DatabaseName := 'OdinSQL';
#     TransferTable.DatabaseName := 'OdinSQL';
#     TransferTable.TableType := ttDefault;
#     if dbReference > '' then
#       TransferTable.TableName := dbReference + '.transfer'
#     else
#       TransferTable.TableName := 'transfer';

#     StudQuerySQL.DatabaseName := 'OdinSQL';
#     StudLookupSQL.DatabaseName := 'OdinSQL';
#     StudentTable.DatabaseName := 'OdinSQL';
#     StudentTable.TableType := ttDefault;

#     CustomRestrictTable.DatabaseName := 'OdinSQL';
#     CustomRestrictTable.TableType := ttDefault;
#     CustomRestrictTable.TableName := 'cstmrsct';

#     if lSQLAction then
#     begin
#       ActionQuery.DatabaseName := 'OdinSQL';
#       ActionTable.DatabaseName := 'OdinSQL';
#       ActionTable.TableType := ttDefault;
#       ActionTable.TableName := 'action';
#       LostQuery.DatabaseName := 'OdinSQL';
#     end;

#     if lSQLInventry then
#     begin
#       InventoryTable.DatabaseName := 'OdinSQL';
#       InventoryTable.TableType := ttDefault;
#       InventoryTable.TableName := 'inventry';
#       InvQuerySQL.DatabaseName := 'OdinSQL';
#     end;

#     if lSQLvendor then
#     begin
#       VendorTable.DatabaseName := 'OdinSQL';
#       VendorTable.TableType := ttDefault;
#       VendorTable.TableName := 'vendor';
#       VendorSQL.DatabaseName := 'OdinSQL';
#     end;
#     if lSQLtuition then
#     begin
#       TuitionTable.DatabaseName := 'OdinSQL';
#       TuitionTable.TableName := 'tuition';
#       TuitionTable.TableType := ttDefault;
#       TuitionSetupTable.DatabaseName := 'OdinSQL';
#       TuitionSetupTable.TableName := 'tuitionsetup';
#       TuitionSetupTable.TableType := ttDefault;
#       TuitionSetupTable.IndexName := 'class';
#       TuitionPlansTable.DatabaseName := 'OdinSQL';
#       TuitionPlansTable.TableName := 'tuitnpayplan';
#       TuitionPlansTable.TableType := ttDefault;
#       TuitnPayTable.DatabaseName := 'OdinSQL';
#       TuitnPayTable.TableName := 'tuitnpay';
#       TuitnPayTable.TableType := ttDefault;
#       TuitnPaySQL.DatabaseName := 'OdinSQL';
#     end;

#     if lSQLdb then
#     begin
#       RightsTable.TableType := ttDefault;
#       RightsTable.DatabaseName := 'OdinSQL';
#       RightsTable.TableName := 'rights';
#       UsersTable.TableType := ttDefault;
#       UsersTable.DatabaseName := 'OdinSQL';
#       UsersTable.TableName := 'users';
#       WebtranTable.TableType := ttDefault;
#       WebtranTable.DatabaseName := 'OdinSQL';
#       WebtranTable.TableName := 'webtran';
#     end;

#     if dbReference > '' then
#       StudentTable.TableName := dbReference + '.student'
#     else if (ServerType = stMS2005) and not lRef_dbo then
#       StudentTable.TableName := 'student'
#     else if (ServerType = stMS2005) then
#       StudentTable.TableName := 'dbo.student'
#     else
#       StudentTable.TableName := 'student';
#     Students.DataSet := StudentTable;

#     try
#       OdinSQL.Connected := True;
#     except
#       ODBCConnectError;
#     end;
#     UseODBC := True;
#     UseSQL := True;
#     UseDBX := False;
#   end

#   else if Driver = DBX then
#   begin
#     OdinSQL.AliasName := 'MyKidsODBC';
#     Schools.Open;
# end

# else
# begin
#   if NewPath > '' then
#   begin
#     Schools.Params.Values['Path'] := NewPath;
#   end;

#   TranQuerySQL.DatabaseName := 'Schools';
#   TransactTable.DatabaseName := 'Schools';
#   TransactTable.TableType := ttDBase;
#   TransactTable.TableName := 'Transact.dbf';

#   TransferQuery.DatabaseName := 'Schools';
#   TransferTable.DatabaseName := 'Schools';
#   TransferTable.TableType := ttDBase;
#   TransferTable.TableName := 'Transfer.dbf';

#   StudQuerySQL.DatabaseName := 'Schools';
#   StudentTable.DatabaseName := 'Schools';
#   StudentTable.TableType := ttDBase;
#   StudentTable.TableName := 'Student.dbf';
#   Students.DataSet := StudentTable;

#   UseSQL := False;
#   UseDBX := False;

#   Schools.Open;
# end;

# Schools.Connected := True;
# SchoolsSession.NetFileDir := bdeDir;

# end;

# end.""")) # Passes


    def test_braceComment(self):
        self.assertTrue(braceComment.parseString("{$IFDEF DBX}").asList()==['{', '$IFDEF DBX', '}'])
        self.assertTrue(braceComment.parseString("{$R *.DFM}").asList()==['{', '$R *.DFM', '}'])
        

if __name__ == "__main__":
    unittest.main()