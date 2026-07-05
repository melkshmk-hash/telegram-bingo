<!DOCTYPE html>
<html lang="am">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ቴሌግራም ቢንጎ</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        body { font-family: Arial, sans-serif; text-align: center; background-color: #1a1a2e; color: white; margin: 0; padding: 20px; }
        h1 { color: #00fff0; margin-bottom: 5px; }
        #user-info { color: #e94560; font-size: 16px; margin-bottom: 15px; }
        .grid { display: grid; grid-template-columns: repeat(5, 1fr); gap: 8px; max-width: 320px; margin: 0 auto; }
        .cell { background: #16213e; border: 2px solid #0f3460; padding: 15px 0; font-size: 18px; font-weight: bold; border-radius: 8px; cursor: pointer; transition: 0.2s; }
        .cell.selected { background-color: #e94560; border-color: #ff6b6b; color: white; }
    </style>
</head>
<body>
    <h1>የቢንጎ ጨዋታ</h1>
    <div id="user-info">ተጫዋች በመጫን ላይ...</div>
    <div class="grid" id="bingo-card"></div>

    <script>
        const tg = window.Telegram.WebApp;
        tg.ready();
        tg.expand();

        if(tg.initDataUnsafe && tg.initDataUnsafe.user) {
            document.getElementById('user-info').innerText = "ሰላም " + tg.initDataUnsafe.user.first_name + "! መልካም ዕድል!";
        } else {
            document.getElementById('user-info').innerText = "ሰላም ተጫዋች! መልካም ዕድል!";
        }

        const card = document.getElementById('bingo-card');
        for (let i = 1; i <= 25; i++) {
            const cell = document.createElement('div');
            cell.className = 'cell';
            if (i === 13) {
                cell.innerText = "FREE";
                cell.classList.add('selected');
            } else {
                cell.innerText = Math.floor(Math.random() * 75) + 1;
                cell.onclick = function() {
                    cell.classList.toggle('selected');
                };
            }
            card.appendChild(cell);
        }
    </script>
</body>
</html>
