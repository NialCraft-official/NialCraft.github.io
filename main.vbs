Set IE = CreateObject("InternetExplorer.Application")
IE.Navigate "about:blank": IE.Width = 800: IE.Height = 600: IE.Left = 200: IE.Top = 100: IE.MenuBar = 0: IE.ToolBar = 0: IE.StatusBar = 0: IE.Visible = 1
Do While IE.ReadyState <> 4: WScript.Sleep 100: Loop
Set Doc = IE.Document: Set Win = Doc.parentWindow
Doc.write "<html><body style='background:#222;margin:0;overflow:hidden;'><canvas id='c' width='800' height='600'></canvas></body></html>"
Set Canvas = Doc.getElementById("c"): Set Ctx = Canvas.getContext("2d")
Dim px, py: px = 4: py = 4
Dim rx, ry: rx = 400 - (9 * 45) / 2: ry = 300 - (9 * 45) / 2

Sub DrawWorld()
    Ctx.clearRect 0, 0, 800, 600
    Ctx.fillStyle = "#888888": Ctx.font = "12px Courier": Ctx.fillText "Nialcraft VBS Engine v1.0", 320, 20
    Dim gx, gy, x1, y1, cl, oc
    For gx = 0 To 8
        For gy = 0 To 8
            x1 = rx + gx * 45: y1 = ry + gy * 45
            If gy < 3 Then
                cl = "#333333": oc = "#2a2a2a"
            ElseIf gy = 3 Then
                cl = "#4CAF50": oc = "#388E3C"
            ElseIf gy < 7 Then
                cl = "#795548": oc = "#5D4037"
            Else
                cl = "#9E9E9E": oc = "#616161"
            End If
            Ctx.fillStyle = cl: Ctx.fillRect x1, y1, 45, 45: Ctx.strokeStyle = oc: Ctx.strokeRect x1, y1, 45, 45
        Next
    Next
    Dim x, y: x = rx + px * 45 + 8: y = ry + py * 45 + 14
    Ctx.fillStyle = "#00BCD4": Ctx.fillRect x, y, 29, 27: Ctx.fillStyle = "#FFC107": Ctx.fillRect x + 6, y - 10, 17, 10
End Sub

Sub SendMove()
    On Error Resume Next
    Set Http = CreateObject("MSXML2.ServerXMLHTTP")
    Http.Open "POST", "http://127.0.0", True
    Http.setRequestHeader "Content-Type", "application/json"
    Http.Send "{""action"":""move"",""x"":" & px & ",""y"":" & py & "}"
End Sub

Sub Win_onkeydown()
    Dim k: k = Win.event.keyCode
    If k = 87 And py > 0 Then py = py - 1
    If k = 83 And py < 8 Then py = py + 1
    If k = 65 And px > 0 Then px = px - 1
    If k = 68 And px < 8 Then px = px + 1
    DrawWorld: SendMove
End Sub

Set Doc.body.onkeydown = GetRef("Win_onkeydown")
DrawWorld

Do While True
    WScript.Sleep 100
    If Err.Number <> 0 Then WScript.Quit
Loop