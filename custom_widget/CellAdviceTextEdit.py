from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout

class CellAdviceTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()

    def update_textedit(self,cell_id):
        rich_text_content = f"""
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
            <style>
                body {{
                    font-size: 24px; 
                    color: white;
                }}
            </style>
        </head>
        <body>
        <p><strong><span style="color: lightcoral;">单电芯AI专家建议智能分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong></p>
        <p><strong><span style="color: lightcoral;">离散性分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_id}号电芯离散性系数为{cell_id},一致性系数为{cell_id},{cell_id}</p>
        <p><strong><span style="color: lightcoral;">析锂分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_id}号电芯<span style="color: lightcoral;"><strong>未发现</strong></span>析锂异常。</p>
        <p><strong><span style="color: lightcoral;">内部温度预测已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_id}号电芯内部温度预测为{cell_id}\u2103,{cell_id}。<br>电芯<span style="color: lightcoral;"><strong>未发现</strong></span> 
        热失控异常。</p>
        </body>
        </html>
        """
        self.setHtml(rich_text_content)
