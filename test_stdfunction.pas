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

function CalcSpending(lDebit: boolean; id, PayCode: string;
  yStart, tStart, tEnd, mStart, mEnd, wStart, wEnd, sDate, eDate: TDateTime;
  nwPeriod, nmPeriod, ntPeriod: byte; CumAllow: currency): TSpendingArray;
var
  nLoc: ShortInt;
  nAmount, xAmt, yAmt: currency;
  a, b, c: currency;
  aPos, x: ShortInt;
  pArray: TSpendingArray;
  temp: AnsiString;
  cPeriod: AnsiChar;
  TDate: TDateTime;
  UseTable: boolean;
  lAccrueAllow: boolean;

begin
  if Odin.Transact.DataSet = Odin.TransactTable then
    UseTable := true
  else
    UseTable := false;

  GetTransactions(id, PayCode, sDate, eDate, 0);
  Odin.Transact.DataSet := Odin.TranQuerySQL;

  for aPos := 0 to 12 do
  begin
    pArray[aPos, 1] := 0; // Spending for area since beginning of year
    pArray[aPos, 2] := 0; // Weekly spending for area
    pArray[aPos, 3] := 0; // Monthly spending for area
    pArray[aPos, 4] := 0; // Term spending for area
    pArray[aPos, 5] := 0; // Remaining for area
    pArray[aPos, 6] := 0; // Absolute spending for area
    pArray[aPos, 7] := 0; // Today's spending for area
  end;

  nLoc := 0;
  nAmount := 0;

  with Odin do
  begin
    // Use index on ID and then set filter for dates
    // Process with loop
    Transact.DataSet.First;
    // DisableContols prevents refresh of data aware components after every move
    Transact.DataSet.DisableControls;
    while not(Transact.DataSet.eof) do
    begin
      // if FDManager.IsConnectionDef('OdinSQL') then
      if Odin.UseSQL then
        TDate := Transact.DataSet.FieldByName('qDate').AsDateTime
      else
        TDate := Transact.DataSet.FieldByName('Date').AsDateTime;
      if (Transact.DataSet.FieldByName('Payment').AsString = PayCode) then
      begin
        nLoc := Transact.DataSet.FieldByName('Location').AsInteger;
        nAmount := Transact.DataSet.FieldByName('Amount').AsCurrency;
        pArray[nLoc, 6] := pArray[nLoc, 6] + nAmount;
        if (TDate >= yStart) then
          pArray[nLoc, 1] := pArray[nLoc, 1] + nAmount;
        if lDebit then
        begin
          cPeriod := GetAreaPeriod(nLoc);
          if cPeriod = 'N' then
            // don't bother adding since debit list remaining

          else if cPeriod = 'D' then
          begin
            // don't bother if daily, since this can't really be done night before
          end

          else if (cPeriod = 'W') and (TDate >= wStart) and (TDate <= wEnd) then
            pArray[nLoc, 2] := pArray[nLoc, 2] + nAmount

          else if (cPeriod = 'M') and (TDate >= mStart) and (TDate <= mEnd) then
            pArray[nLoc, 3] := pArray[nLoc, 3] + nAmount

          else if (cPeriod = 'T') and (TDate >= tStart) and (TDate <= tEnd) then
            pArray[nLoc, 4] := pArray[nLoc, 4] + nAmount
        end;
      end;
      Transact.DataSet.Next;
    end;
    Transact.DataSet.EnableControls;
  end;

  // Don't bother with this if it is just spending summary
  if lDebit then
    // with Odin.StudentTable do begin
    with Odin.Students.DataSet do
    begin
      if FindField('FixedAllow') <> NIL then
      begin
        // boolean can really take 3 values, true, false and not set
        // unless specifically true, assume allowance accrues
        if Odin.UseSQL then
          lAccrueAllow := not(FieldByName('FixedAllow').AsInteger = 1)
        else
          lAccrueAllow := not(FieldByName('FixedAllow').AsBoolean = true);
      end
      else
        lAccrueAllow := true;

      // Now process remaining in Bank
      // cPeriod is restriction period, nAmount is spending limit
      temp := FieldByName('Time_1').AsString;
      if temp = '' then
        cPeriod := ' '
      else
        cPeriod := temp[1];
      nAmount := FieldByName('Area_1').AsFloat;
      if cPeriod = 'W' then
      begin
        xAmt := pArray[1, 2];
        // do not accrue does not respect weeks and months that don't count, which does make it different
        // from other sales areas (which do not accrue)  Could address at some point
        if lAccrueAllow then
          pArray[1, 5] := nAmount * nwPeriod - pArray[1, 1] + CumAllow
        else
          pArray[1, 5] := nAmount - xAmt;
        // When calculating remaining period totals, these need to be adjusted
        // by the cumulative allowance and any surplus in the bank
        // eg bank allowance 20 remaining 45, then add 25 to remaining
        b := pArray[1, 5];
        a := b - nAmount;
        pArray[12, 2] := a;
      end
      else if cPeriod = 'M' then
      begin
        xAmt := pArray[1, 3];
        if lAccrueAllow then
          yAmt := nAmount * nmPeriod - pArray[1, 1] + CumAllow
        else
          yAmt := nAmount - xAmt;
        pArray[1, 5] := yAmt;
        pArray[12, 3] := yAmt - nAmount;
      end
      else if cPeriod = 'T' then
      begin
        xAmt := pArray[1, 4];
        if lAccrueAllow then
          pArray[1, 5] := nAmount * ntPeriod - pArray[1, 1] + CumAllow
        else
          pArray[1, 5] := nAmount - xAmt;
        pArray[12, 4] := pArray[1, 5] - nAmount;
      end
      else if cPeriod = 'N' then
        pArray[1, 5] := 0
      else if cPeriod = 'D' then
        pArray[1, 5] := 0
      else if cPeriod = ' ' then
        pArray[1, 5] := nAmount - pArray[1, 1] + CumAllow
      else
        pArray[1, 5] := nAmount - pArray[1, 1] + CumAllow;

      // Now process remaining in other spending areas
      for aPos := 2 to 10 do
      begin
        x := aPos;
        cPeriod := GetAreaPeriod(x);
        // nAmount := Fields[Floc+offset*aPos-1].AsFloat;
        nAmount := FieldByName('Area_' + IntToStr(aPos)).AsFloat;
        if (cPeriod = 'W') then
        begin
          if nwPeriod = 0 then
            nAmount := 0;
          a := pArray[aPos, 2];
          b := (nAmount - a);
          pArray[aPos, 5] := b;
          c := pArray[11, 2];
          pArray[11, 2] := c + a;
        end
        else if cPeriod = 'M' then
        begin
          if nmPeriod = 0 then
            nAmount := 0;
          pArray[aPos, 5] := (nAmount - pArray[aPos, 3]);
          pArray[11, 3] := pArray[11, 3] + pArray[aPos, 3];
        end
        else if cPeriod = 'T' then
        begin
          if ntPeriod = 0 then
            nAmount := 0;
          pArray[aPos, 5] := (nAmount - pArray[aPos, 4]);
          pArray[11, 4] := pArray[11, 4] + pArray[aPos, 4];
        end
        else if cPeriod = 'N' then
          pArray[aPos, 5] := 0
        else if cPeriod = 'D' then
          pArray[aPos, 5] := 0
        else if cPeriod = ' ' then
          pArray[aPos, 5] := (nAmount - pArray[aPos, 1])
        else
          pArray[aPos, 5] := nAmount;
      end;
    end;

  { if odin.Students.DataSet = odin.StudQuerySQL then
    MessageDlg('StudQuerySQL', mtError, [mbIgnore], 0)
    else if odin.Students.DataSet = odin.StudLookupSQL then
    MessageDlg('StudLookupSQL', mtError, [mbIgnore], 0)
    else if odin.Students.DataSet = odin.StudentTable then
    MessageDlg('StudentTable', mtError, [mbIgnore], 0); }

  // with Odin.StudentTable do begin
  with Odin.Students.DataSet do
  begin
    // Now process weekly, monthly, term totals
    nAmount := FieldByName('Wkly_Allow').AsFloat;
    pArray[12, 2] := pArray[12, 2] + nAmount - pArray[11, 2];
    nAmount := FieldByName('Mnth_Allow').AsFloat;
    pArray[12, 3] := pArray[12, 3] + nAmount - pArray[11, 3];
    nAmount := FieldByName('Term_Allow').AsFloat;
    pArray[12, 4] := pArray[12, 4] + nAmount - pArray[11, 4];
  end;

  if UseTable then
    Odin.Transact.DataSet := Odin.TransactTable;
  result := pArray;
end;