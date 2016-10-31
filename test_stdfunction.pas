function GetMealPlanInfo(var id, cPeriod: string): integer;
var
  temp: string;
  word: integer;
begin
//  // look it up in student
//  // with Odin.LookupQuery do
//  // begin
    // Close;;
//     SQL.Clear;
//     SQL.Add('SELECT Plan_MP,Time_MP');
//     if Odin.UseSQL then
//     begin
//       SQL.Add('FROM student');
//       ConnectionName := 'OdinSQL';
//     end
//     else
//     begin
//       SQL.Add('FROM ":Schools:STUDENT.DBF"');
//       ConnectionName := 'Schools';
//     end;
//     temp := 'WHERE ID_NUMBER = ''' + id + '''';
//     SQL.Add(temp);
//     Prepare;
//     Open;
//     cPeriod := FieldByName('Time_MP').AsString;
//     result := FieldByName('Plan_MP').AsInteger;
//   end;
end;

function GetMeals(var id, cPeriod: string; yStart, tStart, tEnd, mStart, mEnd,
  wStart, wEnd: TDateTime): integer;
var
  sDate, eDate: TDateTime;
  temp, b: string;
begin
//   // look it up in student
//   // look it up in student
//   // look it up in student
end;
