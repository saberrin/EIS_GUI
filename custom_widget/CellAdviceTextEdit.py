from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from database.repository import Repository
class CellAdviceTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.repository = Repository()
        
    def update_textedit(self,cell_id):
        dispersion_rate = None
        dispersion_rate_advice = None
        temperature = None
        temperature_advice = None
        info = self.repository.get_latest_generated_info(cell_id)
        if info:
            dispersion_rate = info['dispersion_rate']
            if dispersion_rate:
                dispersion_rate = round(dispersion_rate,2)
                if dispersion_rate > 0.5:
                    dispersion_rate_advice = "离散度较大，建议及时排查"
                else:
                    dispersion_rate_advice = "电芯离散度在合理区间"
            
            temperature = info['temperature']
            if temperature:
                if temperature > 40:
                    temperature_advice = "电芯内部温度偏高，建议及时排查"
                else:
                    temperature_advice = "电芯内部温度正常"
                    
        rich_text_content = f"""
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
            <style>
                body {{
                    font-size: 18px; 
                    color: white;
                }}
            </style>
        </head>
        <body>
        <p><strong><span style="color: lightcoral;">单电芯AI专家建议智能分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong></p>
        <p><strong><span style="color: lightcoral;">离散性分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_id}号电芯离散性系数为{dispersion_rate},{dispersion_rate_advice}</p>
        <p><strong><span style="color: lightcoral;">析锂分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_id}号电芯<span style="color: lightcoral;"><strong>未发现</strong></span>析锂异常。</p>
        <p><strong><span style="color: lightcoral;">内部温度预测已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_id}号电芯内部温度预测为{temperature}\u2103,{temperature_advice}。<br>电芯<span style="color: lightcoral;"><strong>未发现</strong></span> 
        热失控异常。</p>
        </body>
        </html>
        """
        self.setHtml(rich_text_content)
