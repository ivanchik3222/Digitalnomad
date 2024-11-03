from flask import render_template


def extra():
    return render_template('extra.html')

def resources():
    return render_template('resources.html')


if __name__ == '__main__':
    print("nuh uh")
else:
    print("import static_routes")