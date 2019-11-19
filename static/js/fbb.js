/**
 * Module addes moveable sticky feedback box on each page
 */

//fbb - is an object of the feedbackbox
var fbb = {};

/** Method initializes input elements */
fbb.initInputs = () => {
    const inputs = document.querySelectorAll('.feedback-box__input');
    inputs.forEach(inp => {inp.classList.remove('error'); inp.value = ''});
    const textarea = document.querySelector('.feedback-box__textarea');
    textarea.value = '';
    textarea.classList.remove('error')
}
/** Method for closing up fbb and rerrange it to next opening */
fbb.closeFBBHandler = (evn) => {
    if (fbb && fbb.box){
        fbb.initInputs();
        fbb.openFBBHandler();
        fbb.box.style.display = 'none';
    }
    if (evn){
        (evn.preventDefault) ? evn.preventDefault() : (evn.returnValue = false);
        (evn.stopPropagation) ? evn.stopPropagation() : (evn.cancelBubble = true);
    }
}
/** Method arrage fbb's element and open fbb */
fbb.openFBBHandler = () => {
    if (!fbb || !fbb.box)
        return;
    fbb.initInputs();
    if (fbb.box.style && fbb.box.style.display && fbb.box.style.display === 'block') 
    {
        fbb.box.style.display = 'none';
        fbb.box.removeAttribute('style');    
    }
    else {
        //Locating fbb in special position
        if (!fbb.box.style){
            const att = document.createAttribute('style'); 
            att.value = "position: fixed; right: 200px; bottom: 0; display: block";
            fbb.box.setAttributeNode(att);
        }
        else
            fbb.box.setAttribute('style', "position: fixed; right: 200px; bottom: 0; display: block");
        //fetch new capctha
        fbb.reloadCaptcha();
    };
    //arrange text area
    fbb.alignTextarea();
    //Toggling color of the fbb loader button
    const fbb_loader_caption = document.querySelector('.feedback-box-loader > p')
    st = getComputedStyle(fbb.loader);
    if (st.backgroundColor !== 'rgb(255, 255, 255)'){
        fbb.loader.style.backgroundColor = 'rgb(255, 255, 255)';    
        fbb_loader_caption.style.color = fbb.originColor;
    }
    else{
        fbb.loader.style.backgroundColor = fbb.originColor;
        fbb_loader_caption.style.color = 'rgb(255, 255, 255)';
    }
    const loader_paths = [...document.querySelectorAll('.feedback-box-loader > svg > g > path')];
    loader_paths.forEach(path => {
        if ((path.getAttribute('fill').trim() === '#fff')||(path.getAttribute('fill').trim() === 'rgb(255, 255, 255)'))
            path.setAttribute('fill',  fbb.originColor);
        else
            path.setAttribute('fill', 'rgb(255, 255, 255)');
    });
}
/** Method for checking fbb position on screen.
 * 
 * Intended for 'sticky' feature of the fbb
 */
fbb.isFBBInsideWindow =() => {
    if (fbb){
        const w_size = getClientSize();
        if (fbb.rect.left > 0 && fbb.rect.right < w_size.w && fbb.rect.top > 0 && fbb.rect.bottom < w_size.h)     
            return true;
        return false;
    }
}
/** Implementing 'sticky' feature of the fbb 
 * param {integer} gap - The value of the gap between side of the fbb and screen is than fbb sticks to screen
*/
fbb.restrainFBB = (gap) => {
    gap = gap || 10;
    if (fbb){
        const w_size = fbb.getClientSize();
        fbb.rect = fbb.box.getBoundingClientRect();
        if (w_size.w <= (fbb.rect.right - fbb.rect.left)) {
            fbb.box.style.left = '0';
            fbb.box.style.right = '0';
            fbb.box.style.top = '0';
            fbb.box.style.bottom = '0';
        }  
        if (w_size.h <= (fbb.rect.bottom - fbb.rect.top)) {
            fbb.box.style.top = '0px';
            fbb.box.style.bottom = '0px';
        }  
        if (fbb.rect.left < gap)
            fbb.box.style.left = '0px';
        else if (fbb.rect.right > (w_size.w - gap))
            fbb.box.style.left = ((w_size.w - (fbb.rect.right - fbb.rect.left))<0) ? 0 : (w_size.w - (fbb.rect.right - fbb.rect.left)) + 'px';
        if (fbb.rect.top < gap)
            fbb.box.style.top = '0px';
        else if (fbb.rect.bottom > (w_size.h - gap))
            fbb.box.style.top = ((w_size.h - (fbb.rect.bottom - fbb.rect.top))<0) ? 0 : (w_size.h - (fbb.rect.bottom - fbb.rect.top)) + 'px';
    }
}
/** Allows to capture fbb for moving it around the page */
fbb.mousedownFBBHandler = (evn) => {
    evn = evn || window.event;
    const w_size = fbb.getClientSize();
    fbb.rect = fbb.box.getBoundingClientRect();
    if ((w_size.w <= (fbb.rect.right - fbb.rect.left))&&(w_size.h <= (fbb.rect.bottom - fbb.rect.top))) {
        fbb.captured = false;
        return;
    } 
    fbb.capture_point.x = evn.clientX;
    fbb.capture_point.y = evn.clientY;
    fbb.captured = true;
    fbb.rect = fbb.box.getBoundingClientRect();
    const left = fbb.rect.left+'px';
    const top = fbb.rect.top+'px';
    if (!fbb.box.style){
        const att = document.createAttribute("style"); 
        att.value = "display: block";
        fbb.box.setAttributeNode(att);
    }
    else
        fbb.box.setAttribute('style', "display: block");
    fbb.box.style.left =  left;
    fbb.box.style.top =  top;
}
/** Allows to drop fbb on the page */
fbb.mouseupFBBHandler = (evn) => {
    evn = evn || window.event;
    if (fbb){  
        fbb.captured = false;
        setTimeout(fbb.restrainFBB, 1000, 40);
    }
}
/** Returns size of the active page accept scrollbars sizes */
fbb.getClientSize = (w) => {
    const d = document;
    if (d.compatMode == 'CSS1Compat')
        return {w: d.documentElement.clientWidth, h: d.documentElement.clientHeight};  
    return {w: d.body.clientWidth, h: d.body.clientHeight};  
}
/** Allows moving fbb around the page */
fbb.mousemoveFBBHandler = (evn) => {
    evn = evn || window.event;
    if (fbb && fbb.captured){
        const left = (parseInt(fbb.box.style.left.substring(0, fbb.box.style.left.length - 2)) + (evn.clientX - fbb.capture_point.x)) + 'px';
        const top = (parseInt(fbb.box.style.top.substring(0, fbb.box.style.top.length - 2)) + (evn.clientY - fbb.capture_point.y)) + 'px';
        fbb.capture_point.x = evn.clientX;
        fbb.capture_point.y = evn.clientY;
        fbb.box.style.left =  left;
        fbb.box.style.top =  top;
        fbb.restrainFBB( );
    }
    (evn.preventDefault) ? evn.preventDefault() : (evn.returnValue = false);
    (evn.stopPropagation) ? evn.stopPropagation() : (evn.cancelBubble = true);
}
/** Checks inputs elements and sends message */
fbb.submitFBB = (evn) => {
    evn = evn || window.event;
    let inputs = [...document.querySelectorAll('.feedback-box__input,.feedback-box__textarea')];
    inputs.filter(inp => inp.classList.contains('error') === false).forEach(inp => (inp.value.trim() === '' ? inp.classList.toggle('error') : inp.classList.remove('error')));
    if (!inputs.some(inp => inp.classList.contains('error'))){
        let data = {};
        inputs.reduce((data, inp) => {data[inp.name] = inp.value; return data}, data);
        csrftoken = document.cookie.match(/csrftoken=(\w+)/)[1];
        fetch('/visits/feedback', {credentials: 'same-origin', method: 'POST', cache: 'no-cache', body: JSON.stringify(data), headers: {'X-CSRFToken': csrftoken}})
        .then(response => response.text())
        .then((response) => { 
            document.querySelector('.feedback-box__wrapper').classList.add('finished');
            document.querySelector('.feedback-box__inform-panel').innerText = (response == '1') ? 'Сообщение успешно отправлено!' : 'Ошибка при отправке сообщения!';
        })
        .finally(() => setTimeout(() => {
            document.querySelector('.feedback-box__wrapper').classList.remove('finished');
            document.querySelector('.feedback-box__inform-panel').innerText = ''; 
            fbb.closeFBBHandler()
        }, 3000));
    }
}
/** Empty input elements are not allowed */
fbb.inputKeyHandler = (evn) => {
    env = evn || window.event;
    elem = evn.target || evn.srcElement;
    elem.classList.remove('error');
}
/** Fetching captch image via ajax */
fbb.reloadCaptcha = () => {
    document.getElementById('captcha_input').value = '';
    const captcha_img = document.querySelector('.captcha-img');
    const reload_captcha_btn = document.getElementById('reloadCaptchaBtn');
    reload_captcha_btn.classList.add('invisible');
    fetch('/visits/get_captcha', {credentials: 'same-origin', method: 'GET', cache: 'no-cache'})
    .then(response => response.text())
    .then(response => {captcha_img.outerHTML = '<img class="captcha-img" src="'+response+'"/>';
    })
    .finally( () => {
        reload_captcha_btn.classList.remove('invisible');
    });
}
/** Validation of the inputs before senging message */
fbb.checkField = (evn) => {
    env = evn || window.event;
    elem = evn.target || evn.srcElement;
    if (elem.value === '')
        return;
    if (elem.id == 'captcha_input') {
        if (elem.value.trim() !== ''){
            fetch('/visits/get_captcha?captcha='+elem.value.trim(), {credentials: 'same-origin', method: 'GET', cache: 'no-cache'})
            .then(response => response.text())
            .then(response => (response.trim() === 'False' ? elem.classList.add('error') : elem.classList.remove('error')));
        }
    }
    else if (elem.id == 'client_email') {
        if (!elem.value.trim().match(/^[a-zA-Z0-9\._\-]+@[a-zA-Z0-9\.\-]+\.[a-zA-Z]{2,6}$/)){
            elem.classList.add('error');
        }
        else
        elem.classList.remove('error');
    }
    else if (elem.id == 'client_phone') {
        if (!elem.value.trim().match(/^[0-9 \(\)\-\+,\.]+$/)){
            elem.classList.add('error');
        }
        else
        elem.classList.remove('error');
    }
}

fbb.inputMouseEventHandler = (evn) => {
    evn = evn || window.event;
    (evn.stopPropagation) ? evn.stopPropagation() : (evn.cancelBubble = true);
}
/** Resizing textarea-control  for fitting up the fbb size */
fbb.alignTextarea = () => {
    if (fbb && fbb.box){
        const textarea = document.querySelector('.feedback-box__textarea');
        textarea.style.height = 'auto';
        const btn = document.querySelector('.feedback-box__btn');
        const textarea_styles = window.getComputedStyle(textarea, null);
        let textarea_height = parseInt(textarea_styles.height.substring(0, textarea_styles.height.length - 2));
        do{
            textarea_height += 1;
            textarea.style.height = textarea_height+'px';
            btn_rect = btn.getBoundingClientRect();  
            fbb_rect = fbb.box.getBoundingClientRect();  
        } while (fbb_rect.bottom - btn_rect.bottom > 10);
        fbb.restrainFBB();
    }
}
/** Creating fbb and its loader button */
(function createFeedbackBox(){
    d = document;
    const fbb = d.createElement('form');  
    let attr_autocomplete_off = d.createAttribute('autocomplete');  
    attr_autocomplete_off.value = 'off';
    fbb.setAttributeNode(attr_autocomplete_off);
    let cls = d.createAttribute('class');  
    cls.value = 'feedback-box';
    fbb.setAttributeNode(cls);
    fbb.innerHTML = "<div class='feedback-box__wrapper'><div class='feedback-box__inform-panel'></div><div class='feedback-box__header'><svg id='closeFBB_img' version='1.1' id='Layer_1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' width='512px' height='512px' viewBox='0 0 512 512' xml:space='preserve'><path d='M437.5,386.6L306.9,256l130.6-130.6c14.1-14.1,14.1-36.8,0-50.9c-14.1-14.1-36.8-14.1-50.9,0L256,205.1L125.4,74.5c-14.1-14.1-36.8-14.1-50.9,0c-14.1,14.1-14.1,36.8,0,50.9L205.1,256L74.5,386.6c-14.1,14.1-14.1,36.8,0,50.9c14.1,14.1,36.8,14.1,50.9,0L256,306.9l130.6,130.6c14.1,14.1,36.8,14.1,50.9,0C451.5,423.4,451.5,400.6,437.5,386.6z'/></svg><span class='feedback-box__text_header'>Сообщение</span></div><span class='feedback-box__text'>Вы можете задать нам интересующий Вас вопрос.</span></span><input class='feedback-box__input' type='text' name='user_name' maxlength='50' placeholder='введите имя'/><input id='client_email' class='feedback-box__input' type='email' name='email' maxlength='50' placeholder='email для ответа'/><input id='client_phone' class='feedback-box__input' type='text' name='phone' maxlength='50' placeholder='ваш телефон'/><textarea class='feedback-box__textarea' name='message' maxlength='500' cols='6' wrap='hard' placeholder='ваше сообщение'></textarea><input class='feedback-box__input error' id='captcha_input' type='text' name='captcha' maxlength='12' placeholder='введите код с картинки'/><table><tr><td><img class='captcha-img' src='' alt='captcha' /></td><td><svg id='reloadCaptchaBtn' style='shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd' viewBox='0 0 6.82666 6.82666' xml:space='preserve' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'><defs><style type='text/css'><![CDATA[.fil1 {fill:none}.fil0 {fill:#009ff0;fill-rule:nonzero}]]></style></defs><g id='Layer_x0020_1'><path class='fil0' d='M2.46703 5.54888c0.113677,0.030374 0.230461,-0.0371575 0.260835,-0.150835 0.030374,-0.113677 -0.0371575,-0.230461 -0.150835,-0.260835 -0.466854,-0.125091 -0.838799,-0.427543 -1.06273,-0.815406 -0.223752,-0.387547 -0.299567,-0.860783 -0.174425,-1.32783 0.125091,-0.466854 0.427543,-0.838795 0.815406,-1.06273 0.387547,-0.223752 0.860783,-0.299571 1.32783,-0.174429 0.466854,0.125091 0.838795,0.427543 1.06273,0.815406 0.223752,0.387547 0.299571,0.860783 0.174429,1.32783 -0.030374,0.113677 0.0371575,0.230461 0.150835,0.260835 0.113677,0.030374 0.230461,-0.0371575 0.260835,-0.150835 0.155433,-0.580094 0.0608307,-1.16861 -0.217768,-1.65116 -0.278421,-0.482236 -0.740776,-0.85826 -1.32106,-1.01374 -0.580094,-0.155433 -1.16861,-0.0608307 -1.65116,0.217768 -0.482236,0.278421 -0.85826,0.740776 -1.01374,1.32106 -0.155433,0.580094 -0.0608346,1.16861 0.217764,1.65116 0.278421,0.482236 0.74078,0.85826 1.32106,1.01374z'/><path class='fil0' d='M5.895 3.43303c0.0906654,-0.0745551 0.10372,-0.2085 0.0291654,-0.299165 -0.0745551,-0.0906654 -0.2085,-0.10372 -0.299165,-0.0291654l-0.669823 0.551189 -0.551102 -0.669724c-0.0745551,-0.0906654 -0.2085,-0.10372 -0.299165,-0.0291654 -0.0906654,0.0745551 -0.10372,0.2085 -0.0291654,0.299165l0.674638 0.81985c0.00343307,0.00497244 0.00708661,0.00985039 0.0109961,0.0146024 0.0748622,0.0909764 0.209307,0.104035 0.300283,0.0291732l-0.0005 -0.000606299 0.833839 -0.686154z'/></g><rect class='fil1' height='6.82666' width='6.82666'/></svg></td></tr></table><p class='feedback-box__btn'>Отправить</p></div>";
    (d.documentElement) ? (d.documentElement.appendChild(fbb)) : (d.body.appendChild(fbb));
    fbb_loader = d.createElement('div'); 
    
    inputs = d.querySelectorAll('.feedback-box__wrapper input');
    inputs.forEach(inp => inp.setAttributeNode(attr_autocomplete_off.cloneNode()));

    fbb_loader.innerHTML = "<svg class='feedback-box-loader__img' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink' x='0px' y='0px' viewBox='0 0 1000 1000' enable-background='new 0 0 1000 1000' xml:space='preserve'><metadata> Svg Vector Icons : http://www.onlinewebfonts.com/icon </metadata><g><path fill='#fff' d='M104.1,352.3c12.4,8.7,49.8,34.7,112.1,77.9c62.3,43.2,110.1,76.5,143.3,99.8c3.6,2.6,11.4,8.1,23.2,16.7c11.8,8.6,21.7,15.5,29.5,20.8c7.8,5.3,17.3,11.2,28.4,17.8c11.1,6.6,21.6,11.5,31.4,14.8c9.8,3.3,19,4.9,27.3,4.9h0.6h0.6c8.4,0,17.5-1.6,27.3-4.9c9.8-3.3,20.3-8.2,31.4-14.8c11.1-6.6,20.6-12.5,28.4-17.8c7.8-5.3,17.7-12.2,29.5-20.8c11.8-8.6,19.6-14.1,23.2-16.7c33.5-23.3,118.9-82.6,255.9-177.7c26.6-18.6,48.8-41,66.7-67.3c17.9-26.2,26.8-53.8,26.8-82.6c0-24.1-8.7-44.7-26-61.8c-17.3-17.1-37.8-25.7-61.5-25.7h-805c-28.1,0-49.7,9.5-64.8,28.4c-15.1,19-22.7,42.7-22.7,71.1c0,23,10,47.9,30.1,74.7C60.1,316,81.5,337,104.1,352.3z'/><path fill='#fff' d='M935.3,410.9C815.7,491.8,724.9,554.7,663,599.5c-20.8,15.3-37.6,27.3-50.6,35.8c-12.9,8.6-30.2,17.3-51.7,26.3c-21.5,8.9-41.6,13.4-60.1,13.4H500h-0.6c-18.6,0-38.6-4.5-60.2-13.4c-21.5-8.9-38.7-17.7-51.7-26.3c-12.9-8.6-29.8-20.5-50.6-35.8c-49.2-36.1-139.8-99-271.8-188.7C44.5,397,26,381.1,10,363.3v434.2c0,24.1,8.6,44.7,25.7,61.8C52.8,876.4,73.4,885,97.5,885h805c24.1,0,44.7-8.6,61.8-25.7c17.1-17.1,25.7-37.7,25.7-61.8V363.3C974.3,380.8,956.1,396.6,935.3,410.9z'/></g></svg><p class='feedback-box-loader__text'>задать вопрос</p>";
    cls = d.createAttribute('class');  
    cls.value = 'feedback-box-loader';
    fbb_loader.setAttributeNode(cls);
    (d.documentElement) ? (d.documentElement.appendChild(fbb_loader)) : (d.body.appendChild(fbb_loader));
})();
/** Initilization fbb, its loader, inputs elements, adding event handlers, etc */
(function initFeedbackBox(){
    const box = document.querySelector('.feedback-box');
    if (box){
        fbb.box = box;
        fbb.captured = false;
        fbb.originColor = 'rgb(0, 159, 240)';
        fbb.capture_point = {x: undefined, y: undefined};
        fbb.rect = fbb.box.getBoundingClientRect();
        if (!fbb.box.style){
            const att = document.createAttribute("style"); 
            att.value = '';
            fbb.box.setAttributeNode(att);
        }
        fbb.box.style.left = fbb.rect.left+'px';
        fbb.box.style.top = fbb.rect.top+'px';
        const close_fbb_btn = document.getElementById('closeFBB_img');
        if (close_fbb_btn)
            (close_fbb_btn.addEventListener) ? close_fbb_btn.addEventListener('click', fbb.closeFBBHandler, {capture: false}) : close_fbb_btn.attachEvent('onclick', fbb.closeFBBHandler);
        fbb.loader = document.querySelector('.feedback-box-loader');
        if (fbb.loader)
            (fbb.loader.addEventListener) ? fbb.loader.addEventListener('click', fbb.openFBBHandler) : fbb.loader.attachEvent('onclick', fbb.openFBBHandler);
        const fbb_submit_btn = document.querySelector('.feedback-box__btn');
        if (fbb_submit_btn)
            (fbb_submit_btn.addEventListener) ? fbb_submit_btn.addEventListener('click', fbb.submitFBB) : fbb_submit_btn.attachEvent('onclick', fbb.submitFBB);
        let inputs = [...document.querySelectorAll('.feedback-box__input,.feedback-box__textarea')];
        inputs.forEach(inp => {
            (inp.addEventListener) ? (inp.addEventListener('input', fbb.inputKeyHandler)) : (inp.attachEvent('oninput', fbb.inputKeyHandler));
            (inp.addEventListener) ? (inp.addEventListener('propertychange', fbb.inputKeyHandler)) : (inp.attachEvent('onpropertychange', fbb.inputKeyHandler));
            (inp.addEventListener) ? (inp.addEventListener('keypress', fbb.inputKeyHandler)) : (inp.attachEvent('onkeypress', fbb.inputKeyHandler));
            (inp.addEventListener) ? (inp.addEventListener('mousedown', fbb.inputMouseEventHandler)) : (inp.attachEvent('onmousedown', fbb.inputMouseEventHandler));
            (inp.addEventListener) ? (inp.addEventListener('mouseup', fbb.inputMouseEventHandler)) : (inp.attachEvent('onmouseup', fbb.inputMouseEventHandler));
            (inp.addEventListener) ? (inp.addEventListener('mousemove', fbb.inputMouseEventHandler)) : (inp.attachEvent('onmousemove', fbb.inputMouseEventHandler));
            (inp.addEventListener) ? (inp.addEventListener('blur', fbb.checkField)) : (inp.attachEvent('onblur', fbb.checkField));
        });
        const reload_captcha_btn = document.getElementById('reloadCaptchaBtn');
        (reload_captcha_btn.addEventListener) ? (reload_captcha_btn.addEventListener('click', fbb.reloadCaptcha)) : (reload_captcha_btn.attachEvent('onclick', fbb.reloadCaptcha));
        
        (box.addEventListener) ? box.addEventListener('mousedown', fbb.mousedownFBBHandler) : box.attachEvent('onmousedown', fbb.mousedownFBBHandler);
        (document.addEventListener) ? document.addEventListener('mouseup', fbb.mouseupFBBHandler) : document.attachEvent('onmouseup', fbb.mouseupFBBHandler);
        (document.addEventListener) ? document.addEventListener('mousemove', fbb.mousemoveFBBHandler) : document.attachEvent('onmousemove', fbb.mousemoveFBBHandler);
        (window.addEventListener) ? window.addEventListener('resize', fbb.alignTextarea, true) : window.attachEvent('onresize', fbb.alignTextarea);
    }
})();