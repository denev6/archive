Sub ProcessData()
    Const startCol = 2
    Const endCol = 6
    Const startRow = 3
    Const endRow = 32
    Const tableRange = "B3:F32"
    Const indexCol = 2
    Const labelCol = 4
    Const maxNumCol = 5
    Const numCol = 6

    Dim num as integer

    Call clear("After", tableRange)
    Call copyFiltered(startRow, endRow, startCol, endCol, numCol)

    Sheets("After").Select 
    Range(tableRange).Sort key1:=Range(strCol(labelCol)&startRow), order1:=xlAscending, _
        key2:=Range(strCol(numCol)&startRow), order2:=xlDecending

    '첫 행에 대한 정보 
    startPointer = startRow
    prevLabel = Cells(startRow, labelCol).Value
    partialSum = Cells(startRow, numCol).Value

    For row = startCol+1 To endRow
        currentLabel = Cells(row, labelCol)
        If prevLabel <> currentLabel Then
            endPointer = row - 1
            Call reDistribute(startPointer, endPointer, partialSum, maxNumCol, numCol)
            startPointer = row
            partialSum = 0
        End If

        If currentLabel = "" Then
            '데이터가 없으면
            Exit For
        End If
        prevLabel = currentLabel
        num = Cells(row, numCol).Value
        partialSum = partialSum + num 
    Next
End Sub

Sub Format()
    Const startRow = 3
    Const endRow = 32
    Const numCol = 6

    Sheets("After").Select
    Call hideRows(startRow, endRow, numCol)
    Call writeIndex(startRow, endRow, numCol)
End Sub

Sub showHiddenRows()
    Rows("3:32").Hidden = False
End Sub


Function strCol(col) as String
    strCol = Chr(col + 64)
End Function

Function clear(sheet, range)
    Sheets(sheet).Range(range).ClearContents
End Function

Function copyFiltered(startRow, endRow, startCol, endCol, criterion)
    Dim num as integer
    index = startRow
    For row = startRow To endRow
        num = Sheets("Before").Range(strCol(criterion) & row)
        If num > 0 Then
            Sheets("After").Range(strCol(startCol) & index, strCol(endCol) & index).Value = _
            Sheets("Before").Range(strCol(startCol) & row, strCol(endCol) & row).Value
            index = index + 1
        End If
    Next
End Function

Function reDistribute(startPointer, endPointer, partialSum, criterion, dst)
    Dim maxNum as integer
    For pointer = startPointer To endPointer
        maxNum = Cells(pointer, criterion).Value
        If partialSum = 0 Then
            Cells(pointer, dst).Value = 0
        elseif partialSum > maxNum Then
            Cells(pointer, dst).Value = maxNum
            partialSum = partialSum - maxNum
        else
            Cells(pointer, dst).Value = partialSum
            partialSum = 0
        End If
    Next
End Function

Function writeIndex(startRow, endRow, criterion)
    Dim num as integer
    index = 1
    For row = startRow To endRow
        num = Cells(row, criterion).Value
        If num > 0 Then
            Cells(row, 2).Value = index 
            index = index + 1 
        End If 
    Next
End Function

Function hideRows(startRow, endRow, criterion)
    Dim num as integer
    For row = startRow To endRow
        num = Cells(row, criterion).Value
        If num = 0 Then
            Rows(row).Hidden = True
        End If 
    Next
End Function
