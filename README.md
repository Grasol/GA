# GAASM-Grasol-Architecture- 
<h3>Compiler Grasol Architecture Asembler by Grasol 2019</h3>

GAASM jest częścią "Project CPU Grasol Architectur" gdzie główną częścią projektu jest zbudowanie działającego CPU.
Pisanie programów jak i kompilacja, będzie się odbywać na współczesnym komputerze.
Z procesorem komunikacja będzie się odbywać przez Arduino, w którym będzie sterownik do CPU. 

<p>Code (grasol asm) -> Compiler GAASM -> Driver (Arduino) <-> Grasol CPU or RAM
[schemat głównego założenia całego projektu]</p>

Procesor będzie miał tylko rejestry, dlatego wymagane jest zbudowanie osobno RAMu.
Więc driver będzie przygotowany na łączenie z dodatkowymi portami. Będzie można to wykorzystać na podłączenie dodatkowych urządzeń
np: wyświetlacza itp

Kompilator GAASM pisany jest w Pythonie 3

Cały spis komend oraz dokładnych opisów działań danych elemntów będzie można znaleść w MANUAL-GRASOL-CPU.pdf (GAASM, DRIVER ARDUINO, CPU).
