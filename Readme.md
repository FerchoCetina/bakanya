# Bakanya

__1__ La base para esta api es: http://127.0.0.1:5000/cat-facts/


Obtener un numero determinado de registros tipo cats.

El endpoint se consume con GET y la url debe estar como el siguiente patron

     http://127.0.0.1:5000/cat-facts/{number}
     
 Donde {number} es la cantidad de registros que deseas obtener un valor entre 1-500
 
 Los registros que trae son de cats con update del año actual.
 
 
 ### Respuestas:
 
 Existes varios status de respuesta.
 
 * 200  Todo correcto!!!
 * 204  El parametro number no tiene un digito o es menor a 0
 * 206  Trae los resultados con update del año actual pero la cantidad de resultados son menos a {number}
 
 
 