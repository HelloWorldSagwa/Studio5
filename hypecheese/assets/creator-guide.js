document.querySelectorAll('[data-copy-example]').forEach((button) => {
  button.addEventListener('click', async () => {
    const block = document.getElementById(button.dataset.copyExample);
    const status = button.closest('.manual-example').querySelector('[role="status"]');
    if (!block || !status) return;
    try {
      await navigator.clipboard.writeText(block.textContent);
      status.textContent = '예시를 복사했습니다. 해당 입력칸에 붙여 넣으세요.';
    } catch {
      const range = document.createRange();
      range.selectNodeContents(block);
      const selection = window.getSelection();
      selection.removeAllRanges();
      selection.addRange(range);
      status.textContent = '예시를 선택했습니다. 기기의 복사 기능을 이용하세요.';
    }
  });
});
