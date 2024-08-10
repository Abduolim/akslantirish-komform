from flask import Flask, render_template, request
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)
application = app


@app.route('/')
def main_menu():
    return render_template('index.html')


@app.route('/app1', methods=['GET', 'POST'])
def app1():
    if request.method == 'POST':
        try:
            a = complex(request.form['a'].replace('i', 'j'))
            b = complex(request.form['b'].replace('i', 'j'))
            z = complex(request.form['z'].replace('i', 'j'))
            w = reflection_function(a, b, z)
            n = calculate_result(z, w)

            # Grafik
            z_real, z_imag = np.real(z), np.imag(z)
            w_real, w_imag = np.real(w), np.imag(w)

            # chizma yaratish
            plt.figure(figsize=(10, 5))
            plt.grid(True, linestyle='--', alpha=0.5, which='both', linewidth=0.5)

            # koordinata o'lchami
            real_min = min(z_real, w_real, 0) - 1
            real_max = max(z_real, w_real, 0) + 1
            imag_min = min(z_imag, w_imag, 0) - 1
            imag_max = max(z_imag, w_imag, 0) + 1

            # haqiqiy va mavhum o'qlar
            plt.plot([real_min, real_max], [0, 0], 'k')
            plt.plot([0, 0], [imag_min, imag_max], 'k')

            # Grafik o'lchamini avtomatik qilish
            plt.xlim([real_min, real_max])
            plt.ylim([imag_min, imag_max])

            plt.quiver(0, 0, z_real, z_imag, angles='xy', scale_units='xy', scale=1, color='blue', label='z')
            plt.quiver(0, 0, w_real, w_imag, angles='xy', scale_units='xy', scale=1, color='red', label='w=a•z+b')

            plt.xlabel('Im(z)')
            plt.ylabel('Re(z)')
            plt.legend()

            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
            plt.close()

            # Convert complex numbers from j to i for output
            a_i = complex_to_string(a)
            b_i = complex_to_string(b)
            z_i = complex_to_string(z)
            w_i = complex_to_string(w)

            return render_template('index1.html', a=a_i, b=b_i, z=z_i, w=w_i, plot=img_base64)

        except ValueError as e:
            return render_template('index1.html', error=f"Error: {e}. Please enter valid complex numbers.")
        except Exception as e:
            return render_template('index1.html', error=f"An error occurred: {e}")

    return render_template('index1.html')


def reflection_function(a, b, z):
    return a * z + b


def calculate_result(z, w):
    z_abs = abs(z)
    w_abs = abs(w)

    if w_abs > z_abs:
        return f"The z vector has increased by  {w_abs / z_abs:.3f} times"
    elif w_abs < z_abs:
        return f"The z vector has decreased by  {z_abs / w_abs:.3f} times"
    else:
        return "Did not change."


def complex_to_string(c):
    # Check if both real and imaginary parts are zero
    if c.real == 0 and c.imag == 0:
        return "0"

    # Format the real part
    real_str = f"{c.real:.2f}".rstrip('0').rstrip('.')
    # Format the imaginary part
    imag_str = f"{c.imag:.2f}".rstrip('0').rstrip('.')

    # Check if either part is zero and format accordingly
    if c.real == 0 and c.imag != 0:
        return f"{imag_str}i"
    elif c.imag == 0 and c.real != 0:
        return f"{real_str}"
    elif c.imag >= 0:
        return f"{real_str} + {imag_str}i"
    else:
        return f"{real_str} - {abs(c.imag):.2f}".rstrip('0').rstrip('.') + "i"



@app.route('/app2', methods=['GET', 'POST'])
def app2():
    if request.method == 'POST':
        try:
            a = complex(request.form['a'].replace('i', 'j'))
            b = complex(request.form['b'].replace('i', 'j'))

            n = int(request.form['n'])
            if n < 2:
                raise ValueError("Nuqtalar sonini kamida 2 ta kiriting")

            polygon_points = []
            reflected_points = []

            for i in range(1, n + 1):
                z_str = request.form[f'z{i}'].replace('i', 'j')
                z = complex(z_str)
                polygon_points.append(z)
                reflected = reflection_function(z, a, b)
                reflected_points.append(reflected)

            plt.figure(figsize=(10, 5))

            real_min = min(np.real(polygon_points + reflected_points) + [0]) - 1
            real_max = max(np.real(polygon_points + reflected_points) + [0]) + 1
            imag_min = min(np.imag(polygon_points + reflected_points) + [0]) - 1
            imag_max = max(np.imag(polygon_points + reflected_points) + [0]) + 1

            plt.axhline(0, color='black', linewidth=1)
            plt.axvline(0, color='black', linewidth=1)

            plt.xlim([real_min, real_max])
            plt.ylim([imag_min, imag_max])

            plt.scatter(np.real(polygon_points), np.imag(polygon_points), label="Original Points", marker='o',
                        color='b')
            plt.scatter(np.real(reflected_points), np.imag(reflected_points), label="Final Points",
                        marker='x', color='r')

            polygon_points.append(polygon_points[0])
            reflected_points.append(reflected_points[0])
            plt.plot(np.real(polygon_points), np.imag(polygon_points), 'b--')
            plt.plot(np.real(reflected_points), np.imag(reflected_points), 'r--')

            plt.xlabel('Real')
            plt.ylabel('Imaginary')
            plt.legend()
            if n == 2:
                plt.title("")
            else:
                plt.title(f'')
            plt.grid(True)

            # Save the plot to a BytesIO object
            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
            plt.close()

            polygon_points_i = [complex_to_string(z) for z in polygon_points[:-1]]
            reflected_points_i = [complex_to_string(w) for w in reflected_points[:-1]]

            a_i = complex_to_string(a)
            b_i = complex_to_string(b)

            return render_template('index2.html', plot=img_base64, reflected_points=reflected_points_i,
                                   polygon_points=polygon_points_i, a=a_i, b=b_i)

        except ValueError as e:
            return render_template('index2.html', error=f"Error: {e}. Nuqtalar sonini kamida 2 ta kiriting ")
        except Exception as e:
            return render_template('index2.html', error=f"Xatolik yuz berdi: {e}")

    return render_template('index2.html')


def plot_circle(center, radius, label=None, color='blue'):
    theta = np.linspace(0, 2 * np.pi, 100)
    x = center.real + radius * np.cos(theta)
    y = center.imag + radius * np.sin(theta)
    plt.plot(x, y, label=label, color=color)
    plt.scatter(center.real, center.imag, color=color)


@app.route('/app3', methods=['GET', 'POST'])
def app3():
    if request.method == 'POST':

        o = complex(request.form['center'].replace('i', 'j'))
        r = float(request.form['radius'])
        a = complex(request.form['a'].replace('i', 'j'))
        b = complex(request.form['b'].replace('i', 'j'))

        plt.figure(figsize=(10, 5))
        plot_circle(o, r, label='Original Circle', color='blue')
        plt.grid(True, linestyle='--', alpha=0.7, which='both', linewidth=0.5)

        plt.axhline(0, color='black', linewidth=1)
        plt.axvline(0, color='black', linewidth=1)

        if o != 0:
            new_radius = r * abs(a)
            new_center_shifted = a * o + b
            plot_circle(new_center_shifted, new_radius, label='Final Circle', color='red')

            plt.axis('equal')

            final_circle_center = complex_to_string(new_center_shifted)
            final_circle_radius = str(new_radius)

            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
            plt.close()

            return render_template('index3.html', final_circle_center=final_circle_center, o=complex_to_string(o),
                                   a=complex_to_string(a), b=complex_to_string(b), r=r,
                                   final_circle_radius=final_circle_radius, plot=img_base64)

        else:
            new_radius = r * abs(a)
            new_center_shifted = o + b
            plot_circle(new_center_shifted, new_radius, label='Final Circle', color='red')

            plt.axis('equal')

            final_circle_center = complex_to_string(new_center_shifted)
            final_circle_radius = str(new_radius)

            img_data = BytesIO()
            plt.savefig(img_data, format='png')
            img_data.seek(0)
            img_base64 = base64.b64encode(img_data.read()).decode('utf-8')
            plt.close()

            return render_template('index3.html', final_circle_center=final_circle_center,
                                   final_circle_radius=final_circle_radius, plot=img_base64)

    return render_template('index3.html')


if __name__ == '__main__':
    app.run(debug=True)
