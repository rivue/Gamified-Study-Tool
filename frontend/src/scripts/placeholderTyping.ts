export function startTypingEffect(elem: HTMLInputElement, topics: string[]) {
    let currentIndex = 0;
    let isDeleting = false;
    let text = '';
    let typingSpeed = 75;
    let timer = null;

    function type() {
        let currentTopic = topics[currentIndex];
        const fullText = currentTopic;


        text = isDeleting
            ? fullText.substring(0, text.length - 1)
            : fullText.substring(0, text.length + 1);

        elem.placeholder = text;

        let typeSpeed = typingSpeed;

        if (isDeleting) {
            typeSpeed /= 4;
        }

        if (!isDeleting && text === fullText) {
            typeSpeed = 1500;
            isDeleting = true;
        } else if (isDeleting && text === '') {
            isDeleting = false;
            typeSpeed = 500;
            currentIndex = (currentIndex + (Math.floor(Math.random() * topics.length))) % topics.length;
        }

        clearTimeout(timer);
        timer = setTimeout(type, typeSpeed);
    }

    type();
    return () => clearTimeout(timer);
}

export function stopTypingEffect(stopFunction) {
    stopFunction();
}
