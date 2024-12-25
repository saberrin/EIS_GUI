from PyQt6.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from database.repository import Repository
class PackAdviceTextEdit(QTextEdit):
    def __init__(self):
        super().__init__()
        self.repository = Repository()

    def update_textedit(self,lists):

        max_dispersion_rate = float('-inf')  
        max_temperature = float('-inf')  
        cell_with_max_dispersion_rate = None  
        cell_with_max_temperature = None  
        max_temperature_value = None  
        for cell_id in lists:
            print(f"cell_id:{cell_id}")
            info = self.repository.get_latest_generated_info(cell_id)
            if info:  
                print(f"info:{info}")
                if info['dispersion_rate'] > max_dispersion_rate:
                    max_dispersion_rate = info['dispersion_rate']
                    cell_with_max_dispersion_rate = info['cell_id']
                if info['temperature'] > max_temperature:
                    max_temperature = info['temperature']
                    cell_with_max_temperature = info['cell_id']
                    max_temperature_value = info['temperature']

        rich_text_content = f"""
        <html lang="zh">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title></title>
            <style>
                body {{
                    font-size: 16px; 
                    color: white;
                }}
            </style>
        </head>
        <body>
        <p><strong><span style="color: lightcoral;">AI专家建议智能分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong></p>
        <p><strong><span style="color: lightcoral;">离散性分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_with_max_dispersion_rate}号电芯离散性偏大,建议及时排查！<br>{cell_with_max_dispersion_rate}号电芯一致性偏低,建议及时排查！</p>
        <p><strong><span style="color: lightcoral;">析锂分析已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        所有检测电芯<span style="color: lightcoral;"><strong>未发现</strong></span>析锂异常。</p>
        <p><strong><span style="color: lightcoral;">内部温度预测已完成<span style="color: lightgreen;"><strong>\u2714</strong></span></span></strong>: <br>
        {cell_with_max_temperature}号电芯温度较高（{max_temperature_value}\u2103）,其余电芯温度正常。<br>所有检测电芯<span style="color: lightcoral;"><strong>未发现</strong></span> 
        热失控异常。</p>
        </body>
        </html>
        """
        self.setHtml(rich_text_content)

