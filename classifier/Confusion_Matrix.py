# ******** PARTE 2: METRICAS DE DESEMPEÑO MATRIZ DE CONFUSION *******
# Se mide la eficacia del modelo respecto a los resultados arrojados
# Se utiliza la libreria sklearn para poder implementar sus utilidades
import numpy as np 
import pandas as pd 
from keras.preprocessing.image import ImageDataGenerator
from keras.models import load_model
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve, auc, roc_auc_score
import matplotlib.pyplot as plt 

# Se coloca la ruta del conjunto de validacion para poder medir la eficacia de las predicciones
test_path = 'C:/Users/saulu/Documents/binary_classifier/classifier/conjunto_de_datos/conjunto_de_pruebas'

# Cargamos el modelo
modelo = load_model('C:/Users/saulu/Documents/binary_classifier/classifier/DATOS_RED/Modelo.h5')

# Se convierten los valores a punto flotante, y se crea un generador para hacer las pruebas ya que el modelo 
# fue creado usando generadores
test_datagen = ImageDataGenerator(rescale=1./255)

test_generator = test_datagen.flow_from_directory(
        test_path,    # el tamaño de el directorio es 500
        target_size=(200, 200),
        batch_size=32,
        class_mode='binary',
        shuffle=False)


# Se realiza la prediccion pasando el generador, y el numero de pasos
# si este resultado es mayor a 0.5, sera Sano, sino es Enfermo, el resultado es convertido a entero 0 o 1
# de manera implicita los pasos son obtenidos dividiendo el tamaño del conjunto entre el batch size
prediccion = (modelo.predict(test_generator, verbose=1)>0.5).astype('int32') # Se crea el GENERADOR con la prediccion

# Creamos la grafica ROC
fpr, tpr, _ = roc_curve(test_generator.classes, prediccion)
roc_auc = auc(fpr, tpr)

plt.figure()
lw = 2
plt.plot(fpr, tpr, color='darkorange',
         lw=lw, label='ROC curve (area = %0.2f)' % roc_auc)
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.savefig('C:/Users/saulu/Documents/binary_classifier/classifier/METRICAS/GraficaROC.png')
plt.show()


print('El tamaño del generador es: ', len(prediccion)) # Muestra el total de predicciones generadas desde la ruta 
print(prediccion) # Muestra el valor de cada prediccion en un arreglo 2D [[1],[0],...]

filenames = test_generator.filenames  # Muestra el nombre de la carpeta y el archivo [Enfermos/enf.jpg]

# Recorremos las imagenes y asignamos etiquetas a las clases 0 Enfermos y 1 Sanos
real = []   

for fila in range(0, 250):
    real.append(0)
    if fila == 249:
        for fila in range(249, 499):
            real.append(1) 

print(real) # valores reales (y_true)


print()
print()
print("Tamaño de array objetivo: ", len(real))
print()

# Se crea un excel que almacena las predicciones por cada imagen, las columnas son
# el nombre de los archivos, las predicciones obtenidas de [:,0], lo cual toma del generador 2D llamado predicciones,
# el valor que este en la posicion 0 de todos los vectores contenidos en el, que en este caso solo es un dato [[1],[0],..]
# y la columna class que contiene las clases reales, este como es una lista comun, se obtienen todos los elementos con [:]
# el excel es posteriormente se guarda en la carpeta MODELO
results = pd.DataFrame({"file":filenames, "pr":prediccion[:,0], "class":real[:]})
results.to_excel('C:/Users/saulu/Documents/binary_classifier/classifier/METRICAS/Predicciones.xlsx', sheet_name='Resultados de las Predicciones')
print(results)



print("------------------------ MATRIZ POR PANDAS---------------")

data = {'y_Actual': real, 'y_Predicted': prediccion[:,0]}

df = pd.DataFrame(data, columns=['y_Actual', 'y_Predicted'])

confusion_matriz = pd.crosstab(df['y_Actual'], df['y_Predicted'], rownames=['Actual'], colnames=['Predicted'])
print(confusion_matriz)



##------------------------ MATRIZ DE SKLEARN------------------------
print("-----------------Matriz SKLEARN")
print()


cm= confusion_matrix(real, prediccion)
print(cm)
clases = ['Sick: 0', 'Healthy: 1']
report= classification_report(real, prediccion, target_names=clases)
print(report)

print("-----------------METRICAS DE MATRIZ DE CONFUSION (SKLEARN)--------------")
print()
ac = accuracy_score(real, prediccion)   #exactitud
print('Puntaje de Precision: ', ac)
rc = recall_score(real,prediccion,average=None)  #recordar
print('Puntaje de Recuperacion: ', rc)
ps = precision_score(real,prediccion,average=None) #precision
print('Puntaje de Presicion', ps)
f1 = f1_score(real,prediccion,average=None)  # puntuacion f1 medida de precision y robustez del modelo
print('Puntaje F1: ', f1)


######### Se Guardan Las Metricas en un Archivo de Texto ##########
archivoPuntajes = open('C:/Users/saulu/Documents/binary_classifier/classifier/METRICAS/Scores.txt', 'w')
archivoPuntajes.write('Puntaje de Clasificación de Precisión: ' + str(ac) + '\n')
archivoPuntajes.write('\n')
archivoPuntajes.write('Puntaje de Recuperación: ' + str(rc) + '\n')
archivoPuntajes.write('\n')
archivoPuntajes.write('Puntaje de Precisión TP/(TP + FP): ' + str(ps) + '\n')
archivoPuntajes.write('\n')
archivoPuntajes.write('Puntaje F1: ' + str(f1))
archivoPuntajes.close()

print("-------------Matriz GRAFICA-----------------")

plt.clf()
plt.imshow(cm, interpolation='nearest', cmap= plt.cm.get_cmap('ocean_r'))
classNames = ['Sick','Healthy']
plt.title('Matriz de confusión set de Validación')
plt.ylabel('respuesta')
plt.xlabel('predicción')
tick_marks = np.arange(len(classNames))
plt.xticks(tick_marks, classNames, rotation=45)
plt.yticks(tick_marks, classNames)
for fila in range(2):
    for columna in range(2):
        plt.text(columna,fila, str(cm[fila][columna]))
plt.savefig('C:/Users/saulu/Documents/binary_classifier/classifier/METRICAS/MatrizConfusion.png')
plt.show()
plt.close()
