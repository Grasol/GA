# GAASM-Grasol-Architecture- 
<h3>Compiler Grasol Architecture Asembler by Grasol 2019</h3>

GAASM jest częścią "Project CPU Grasol Architectur" gdzie główną częścią projektu jest zbudowanie działającego CPU.
Pisanie programów jak i kompilacja, będzie odbywać się na współczesnym komputerze.
Z procesorem komunikować się będzie "sterowonik" CPU zaprogramowany w Arduino. 

<p>Code (grasol asm) -> Compiler GAASM -> Driver (Arduino) <-> Grasol CPU or RAM
[schemat głównego założenia całego projektu]</p>

Procesor został zaprojektowany tylko z rejestrami, dlatego wymagane jest zbudowanie osobno RAMu.
Więc driver będzie przygotowany na łączenie z dodatkowymi portami. Będzie można to wykorzystać na podłączenie dodatkowych urządzeń
np: wyświetlacza itp

Kompilator GAASM pisany jest w Pythonie 3

Cały spis instrukcji oraz dokładnych opisów działań danych elemntów będzie można znaleść w MANUAL-GRASOL-CPU.pdf (GAASM, DRIVER ARDUINO, CPU).
