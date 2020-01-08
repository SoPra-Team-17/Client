# Client


## Isometric View
Transformation von World-Koordinaten zu View-Koordinaten:  
Hierbei bezeichnet
* v : View-Koordinaten
* b : Breite der Tiles
* h : Höhe der Tiles
* x,y,z : World-Koordinaten
![equation](https://latex.codecogs.com/gif.latex?v%20%3D%20%5Cbegin%7Bbmatrix%7D%20v_x%5C%5Cv_y%20%5Cend%7Bbmatrix%7D%20%3D%20%5Cfrac%7B1%7D%7B2%7D%5Cbegin%7Bbmatrix%7D%20b%20%26%20-h%20%26%200%5C%5C%20%5Cfrac%7Bb%7D%7B2%7D%20%26%20%5Cfrac%7Bh%7D%7B2%7D%20%26%20-%20h%20%5Cend%7Bbmatrix%7D%20%5Ccdot%20%5Cbegin%7Bbmatrix%7Dx%5C%5Cy%5C%5Cz%20%5Cend%7Bbmatrix%7D)
