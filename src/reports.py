from datetime import datetime
from functools import wraps
from pathlib import Path
from typing import Callable, Optional

import pandas as pd
from openpyxl.styles.builtins import output


def report_to_file(filename: str | None = None,):
    """
    Декоратор для записи результат отчетов в файл.

    Если имя файла не задано, создается файл с названиемм по умолчанию.
    """

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)

            output_filename = filename

            if output_filename is None:
                output_filename = f'{func.__name__}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'

            output_path = Path(output_filename)

            if isinstance(result, pd.DataFrame):
                result.to_json(
                    output_path,
                    orient='records',
                    force_ascii=False,
                    indent=4
                )
            else:
                output_path.write_text(
                    str(result),
                    encoding='utf-8',
                )

            return result
        return wrapper
    return decorator