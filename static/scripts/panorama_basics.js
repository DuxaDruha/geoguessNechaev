ymaps.ready(function () {
    // Для начала проверим, поддерживает ли плеер браузер пользователя.
    if (!ymaps.panorama.isSupported()) {
        // Если нет, то просто ничего не будем делать.
        console.log("Browser doesn't support panorama");
        return
    }
    // Из файла "static/coordinates/chosen.txt" берем координату
    const fs = require('fs')
    fs.readFile('static/coordinates/chosen.txt', (err, inputD) => {
       if (err) throw err;
          console.log(inputD.toString());
    })
    // Ищем панораму в переданной точке.
    ymaps.panorama.locate([55.744667, 37.541111]).done(
        function (panoramas) {
            // Убеждаемся, что найдена хотя бы одна панорама.
            if (panoramas.length > 0) {
                // Создаем плеер с одной из полученных панорам.
                var player = new ymaps.panorama.Player(
                        'player1',
                        // Панорамы в ответе отсортированы по расстоянию
                        // от переданной в panorama.locate точки. Выбираем первую,
                        // она будет ближайшей.
                        panoramas[0],
                        // Зададим направление взгляда, отличное от значения
                        // по умолчанию.
                        { direction: [315, 12], controls: [''] }
                    );
            }
        },
        function (error) {
            // Если что-то пошло не так, сообщим об этом пользователю.
            alert(error.message);
        }
    );
});