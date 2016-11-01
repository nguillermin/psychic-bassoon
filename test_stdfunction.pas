function GetMealPlanInfo(var id, cPeriod: string): integer;
var
  temp: string;
  word: integer;
begin
 // look it up in student
 // with Odin.LookupQuery do
 begin
    Close;;
    SQL.Clear;
    SQL.Add('SELECT Plan_MP,Time_MP');
    if Odin.UseSQL then
    begin
      SQL.Add('FROM student');
      ConnectionName := 'OdinSQL';
    end
    else
    begin
      SQL.Add('FROM ":Schools:STUDENT.DBF"');
      ConnectionName := 'Schools';
    end;
    temp := 'WHERE ID_NUMBER = ''' + id + '''';
    SQL.Add(temp);
    Prepare;
    Open;
    cPeriod := FieldByName('Time_MP').AsString;
    result := FieldByName('Plan_MP').AsInteger;
  end;
end;

function GetMeals(var id, cPeriod: string; yStart, tStart, tEnd, mStart, mEnd,
  wStart, wEnd: TDateTime): integer;
var
  sDate, eDate: TDateTime;
  temp, b: string;
begin
  if (cPeriod = '') or (cPeriod = 'N') then
  begin
    sDate := yStart;
    eDate := Now;
  end
  else if cPeriod = 'D' then
  begin
    sDate := Now;
  end
  else if cPeriod = 'W' then
  begin
    sDate := wStart;
    eDate := wEnd;
  end
  else if cPeriod = 'M' then
  begin
    sDate := mStart;
    eDate := mEnd;
  end
  else if cPeriod = 'T' then
  begin
    sDate := tStart;
    eDate := tEnd;
  end;

  with Odin.MealsQuery do
  begin
    Close;;
    SQL.Clear;
    SQL.Add('SELECT *');
    if Odin.UseSQL then
    begin
      SQL.Add('FROM meals');
      ConnectionName := 'OdinSQL';
    end
    else
    begin
      SQL.Add('FROM ":Schools:MEALS.DBF"');
      ConnectionName := 'Schools';
    end;
    temp := 'WHERE ID_NUMBER = ''' + id + '''';
    SQL.Add(temp);
    if cPeriod = 'D' then
    begin
      temp := 'AND qdate = ' + '''' + DateToStrSQL(sDate, Odin.UseSQL) + '''';
      SQL.Add(temp);
    end
    else
    begin
      temp := 'AND qdate >= ' + '''' + DateToStrSQL(sDate, Odin.UseSQL) + '''';
      SQL.Add(temp);
      temp := 'AND qdate <= ' + '''' + DateToStrSQL(eDate, Odin.UseSQL) + '''';
      SQL.Add(temp);
    end;
    Prepare;
    Open;
  end;
end;

function GetMeals(var id, cPeriod: string; yStart, tStart, tEnd, mStart, mEnd,
  wStart, wEnd: TDateTime): integer;
var
  sDate, eDate: TDateTime;
  temp, b: string;
begin
  if (cPeriod = '') or (cPeriod = 'N') then
  begin
    sDate := yStart;
    eDate := Now;
  end
  else if cPeriod = 'D' then
  begin
    sDate := Now;
  end
  else if cPeriod = 'W' then
  begin
    sDate := wStart;
    eDate := wEnd;
  end
  else if cPeriod = 'M' then
  begin
    sDate := mStart;
    eDate := mEnd;
  end
  else if cPeriod = 'T' then
  begin
    sDate := tStart;
    eDate := tEnd;
  end;

  with Odin.MealsQuery do
  begin
    Close;;
    SQL.Clear;
    SQL.Add('SELECT *');
    if Odin.UseSQL then
    begin
      SQL.Add('FROM meals');
      ConnectionName := 'OdinSQL';
    end
    else
    begin
      SQL.Add('FROM ":Schools:MEALS.DBF"');
      ConnectionName := 'Schools';
    end;
    temp := 'WHERE ID_NUMBER = ''' + id + '''';
    SQL.Add(temp);
    if cPeriod = 'D' then
    begin
      temp := 'AND qdate = ' + '''' + DateToStrSQL(sDate, Odin.UseSQL) + '''';
      SQL.Add(temp);
    end
    else
    begin
      temp := 'AND qdate >= ' + '''' + DateToStrSQL(sDate, Odin.UseSQL) + '''';
      SQL.Add(temp);
      temp := 'AND qdate <= ' + '''' + DateToStrSQL(eDate, Odin.UseSQL) + '''';
      SQL.Add(temp);
    end;
    Prepare;
    Open;
  end;
end;

procedure SaveFilterStrings(const NewEntry: string);
var
  WorkIni: TIniFile;
  IniStrings: TStrings;
  tStr: string;
  loc: integer;
  lExists: boolean;
begin
  lExists := false;
  IniStrings := TStringList.Create;

  // OpenWorkstationConfig(WorkIni);
  WorkIni := TIniFile.Create(GetWorkIniPath);
  WorkIni.ReadSectionValues('Filters', IniStrings);
  // check whether that string already exists, if it does then ignore
  for loc := 1 to 18 do
  begin
    tStr := IniStrings.Values[IntToStr(loc)];
    lExists := (tStr = NewEntry);
    if lExists then
      Exit;
  end;

  if not lExists then
  begin
    // add filter condition to the list, move all else down
    for loc := 1 to 17 do
    begin
      tStr := IniStrings.Values[IntToStr(loc)];
      WorkIni.WriteString('Filters', IntToStr(loc + 1), tStr);
    end;
    WorkIni.WriteString('Filters', '1', NewEntry);
  end;

  IniStrings.Free;
  WorkIni.Free;
end;