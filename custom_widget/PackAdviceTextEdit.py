from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout

class PackAdviceTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        

    def update_textedit(self):
        rich_text_content = """
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
            <style>
                body {
                    font-size: 20px; 
                    color: white;
                }
            </style>
        </head>
        <body>
        <p><strong><span style="color: lightcoral;">AI专家建议智能分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong></p>
        <p><strong><span style="color: lightcoral;">离散性分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        XX号电芯离散性偏大,建议及时排查！<br>XX号电芯一致性偏低,建议及时排查！</p>
        <p><strong><span style="color: lightcoral;">析锂分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        所有检测电芯<span style="color: lightcoral;"><strong>未发现</strong></span>析锂异常。</p>
        <p><strong><span style="color: lightcoral;">内部温度预测已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        XX号电芯温度较高（40\u2103）,其余电芯温度正常。<br>所有检测电芯<span style="color: lightcoral;"><strong>未发现</strong></span> 
        热失控异常。</p>
        </body>
        </html>
        """
        self.setHtml(rich_text_content)

