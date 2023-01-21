smatr_device предназначен для управления свдигом полотна жалюзи. Оно разработано на языке программирования Pyhton. Состоит из 2 частей: сервер и клиент.

Сначала создайте XML-файл с именем «smart_device.xml» в том же каталоге, что и файлы серверного и клиентского приложений, в следующем формате:

"<smart_device>"
"<shift> 0 </shift>"
"<light> 0 </light>"
"<brightness> 0 </brightness>"
"</smart_device>"

В нем будет храниться текущий статус устройства, и он имеет следующие параметры:
сдвиг: целочисленное значение от 0 до 100, представляющее процентное смещение устройства.
свет: целочисленное значение от 0 до 100, представляющее процент освещенности устройства.
яркость: целочисленное значение от 0 до 50000, представляющее текущую яркость устройства.

Замечание: если файл XML не существует, программа вызовет ошибку при попытке его прочтения, или если значения внутри файла не находятся в указанном диапазоне, программа вызовет ошибку при попытке обновления.
Скачайте файлы серверного и клиентского приложений.

Запустите файл серверного приложения, выполнив команду «python3 tppo_server_5411.py».

Этот файл начнет работать в фоновом режиме и будет проверять состояние устройства каждые 10 секунд и уведомлять клиентов о любых изменениях в устройстве.

Запустите файл клиентского приложения, выполнив команду «python3 tppo_client_5411.py».

Этот файл клиентского приложения предложит Вам ввести запрос. Вы можете либо ввести «set», а затем три целых числа для сдвига, света и яркости, чтобы обновить статус устройства, либо «get», чтобы получить текущий статус устройства.

Вы можете отправлять запросы с нескольких клиентов, каждый из них сможет отправлять запросы и получать ответы от сервера.

Для остановки сервера нужно нажать «CTRL+C».
