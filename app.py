from flask import Flask, request, render_template, redirect, url_for
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Set default values for a, b, c, and d
default_coeffs = {'a': {'val': -100.0, 'name': 'a'},
                  'b': {'val': -50.0, 'name': 'b'},
                  'c': {'val': 1.0, 'name': 'c'},
                  'd': {'val': 1.0, 'name': 'd'}
                  }


def generate_polynomial_latex(coefficients):
    n = len(coefficients) - 1
    terms = []
    for i, coeff in enumerate(reversed(coefficients)):
        if coeff != 0.0:
            if i == 0 and coeff != 0:
                term = str(coeff)
            elif i == 1.0:
                if coeff < 0.0 and coeff != -1.0:
                    term = f"{coeff}x"
                elif coeff == -1.0:
                    term = "-x"
                elif coeff == 1.0 :
                    term = "+x"
                else:
                    term = f"{coeff}x" if not terms else f"+{coeff}x"
            else:
                if coeff < 0.0 and coeff != -1.0:
                    term = f"{coeff}x^{{{i}}}"
                elif coeff == -1.0:
                    term = f"-x^{{{i}}}"
                elif coeff == 1.0:
                    term = f"+x^{{{i}}}"
                else:
                    term = f"+{coeff}x^{{{i}}}"
            terms.append(term)
    if not terms:
        return "f(x) = 0"
    else:
        polynomial = "f(x) = " + " ".join(terms)
        return polynomial



@app.route('/', methods=['GET', 'POST'])
def home():
    global default_coeffs
    f_x = ""

    # Update coefficients if they were submitted in the form
    default_coeffs['a']['val'] = float(request.form.get('a', default_coeffs['a']['val']))
    default_coeffs['b']['val'] = float(request.form.get('b', default_coeffs['b']['val']))
    default_coeffs['c']['val'] = float(request.form.get('c', default_coeffs['c']['val']))
    default_coeffs['d']['val'] = float(request.form.get('d', default_coeffs['d']['val']))

    # Generate LaTeX expression for updated polynomial
    coeffs = [default_coeffs[k]['val'] for k in ['d', 'c', 'b', 'a']]
    f_x = generate_polynomial_latex(coeffs)

    # Generate plot
    x = np.linspace(-10, 10, 1000)
    y = np.polyval(coeffs, x)
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.axhline(0, color='black', lw=1)
    ax.axvline(0, color='black', lw=1)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.grid(True)

    # Encode plot image as base64 string for display in template
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode()

    if request.method == 'POST':
        return render_template('index.html', f_x=f_x, image_data=image_data,
                               default_coeffs=default_coeffs)
    else:
        # Render default polynomial
        return render_template('index.html', f_x=f_x, image_data=image_data, default_coeffs=default_coeffs)


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    global default_coeffs
    default_coeffs = {'a': {'val': -100.0, 'name': 'a'},
                      'b': {'val': -50.0, 'name': 'b'},
                      'c': {'val': 1.0, 'name': 'c'},
                      'd': {'val': 1.0, 'name': 'd'}
                      }
    return render_template('index.html', default_coeffs=default_coeffs)
    # return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
