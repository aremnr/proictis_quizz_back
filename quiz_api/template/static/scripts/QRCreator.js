﻿/*
  Генератор QR-кодов
*/
"use strict";
import { DataQR } from "./DataQr.js";
import { controlOptionsCreator } from "./controlOptionsCreator.js";
//const {controlOptionsCreator} = require('controlOptionsCreator');

//const DataQR = require('DataQr');
/*
 параметры:
   text - кодируемая текстовая строка UTF-8
   [options], по умолчанию: { mode: -1,  eccl: -1, version: -1, mask: -1,
                              image: 'PNG', modsize: -1, margin: -1}
     // - параметры формирования:
     options.mode - метод кодирования: 1 -числовой, 2-буквенно-цифровой, 4-октетный
               если не указан или -1, то выбирается допустимый метод
     options.eccl -  уровень коррекции ошибок: 1(L), 0(M), 3(Q), 2(H)
               если не указан или -1, то подбор допустимого уровня начиная с 3(Q)
     options.version - версия: целое число в [1,40]
               если не указан или -1, то выбирается наименьшая возможная версия
     options.mask: - шаблон маски: целое число в [0,7],
                если не указан или -1, то выбирается лучшая маска

     // - параметры результата:
     options.image: - формат изображения: регистронезависимая строка:
                одна из 'PNG', 'SVG','HTML' или 'NONE' (не формировать изображение),
                если не указан, то результат выводится в формате 'PNG'
     options.modsize: - размер модуля ( modsize x modsize ): целое число больше 1 ,
                 если не указан или -1, то 4
     options.margin:  - размер свободной зоны в модулях: целое число от 0,
                если не указан, то 4 модуля

  возвращает объект { ... }:
      где
        // исходный текст
        text,
        // параметры сформированного QR-кода
        mode, eccl, version, mask, image, modsize, margin,
        // массив - матрица QR-кода в 0-белый, 1-черный
        matrix,
        // HTML изображения QR-кода в заданом формате или '' в случае ошибки
        // или когда был задан параметр image === 'NONE'
        result,
        // имя параметра, вызвавшего ошибку или '' при отстутствии ошибок
        // код, код, поясняющий ошибку или '' при отстутствии ошибок
        errorSubcode
 */
window.QRCreator = (text = '', options = {}) => {
  const qrcode = new DataQR(text, options);

  // контроль опций для генерации QR-кода
  controlOptionsCreator(qrcode);
  if (!qrcode.error) {
    // этапы формирования QR-кода:
    // - формирование кодовых слов данных (без битов ECC)
    qrcode.dataToCodewords();
    // - формирование кодовых слов для размещения в QR-коде (группировка с ЕСС)
    qrcode.makeCodewordsQR();
    // - формирование матрицы QR-кода
    qrcode.makeMatrix();
  }

  return qrcode.report();
};
