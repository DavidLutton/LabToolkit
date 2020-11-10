from IPython.display import HTML


def table(data):
    return HTML(
        '<table><tr>{}</tr></table>'.format('</tr><tr>'.join(
           '<td>{}</td>'.format('</td><td>'.join(str(_) for _ in row)) for row in data))
       )
