// static/js/academics/subject_list.js

function toggleAccordion(header) {
    const card = header.parentElement;
    const currentContent = card.querySelector('.accordion-content');
    const currentIcon = header.querySelector('.chevron-icon');

    const isOpen = currentContent.style.maxHeight && currentContent.style.maxHeight !== '0px';

    // Close ALL other accordions
    document.querySelectorAll('.accordion-content').forEach(content => {
        if (content !== currentContent) {
            content.style.maxHeight = '0px';
            content.style.opacity = '0';
            const otherHeader = content.parentElement.querySelector('div[onclick]');
            if (otherHeader) {
                const otherIcon = otherHeader.querySelector('.chevron-icon');
                if (otherIcon) otherIcon.style.transform = 'rotate(0deg)';
            }
        }
    });

    // Toggle current
    if (isOpen) {
        currentContent.style.maxHeight = '0px';
        currentContent.style.opacity = '0';
        currentIcon.style.transform = 'rotate(0deg)';
    } else {
        currentContent.style.maxHeight = currentContent.scrollHeight + 'px';
        currentContent.style.opacity = '1';
        currentIcon.style.transform = 'rotate(180deg)';
    }
}
