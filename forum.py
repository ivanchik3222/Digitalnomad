from flask import render_template

def forum():
    return render_template('forum.html')

if __name__ == '__main__':
    print("nuh uh")
else:
    print("import forum")