from flask import jsonify, render_template
from filoModules.Debug import Debug


debug = Debug("Returns")
class Returns:
    @staticmethod
    def return_message(title, content, r_time, r_url):
        debug.print_d(f"Returning message | title:{title},content:{content},r_time:{r_time},r_url:{r_url}")
        return render_template("webapp/alert.html",
            title=str(title),
            content=str(content),
            r_time=str(r_time),
            r_url=str(r_url)
        )