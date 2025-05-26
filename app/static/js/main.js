/**
 * File JavaScript untuk Aplikasi Web Peningkatan Kualitas Gambar
 */

document.addEventListener('DOMContentLoaded', function() {
    // Fungsi untuk menampilkan preview gambar
    const imageInput = document.getElementById('image');
    if (imageInput) {
        imageInput.addEventListener('change', function(e) {
            showImagePreview(this);
        });
    }
    
    // Setup area upload dengan drag and drop
    setupDragAndDrop();
    
    // Setup slider parameter filter
    setupSliders();
});

/**
 * Menampilkan preview gambar yang diunggah
 * @param {HTMLInputElement} input - Input file
 */
function showImagePreview(input) {
    const uploadArea = document.getElementById('upload-area');
    const preview = document.getElementById('preview');
    const uploadContent = document.querySelector('.upload-content');
    
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            preview.src = e.target.result;
            preview.classList.remove('hidden');
            uploadContent.classList.add('hidden');
            uploadArea.style.border = '2px solid #0d6efd';
        }
        
        reader.readAsDataURL(input.files[0]);
    }
}

/**
 * Mengatur fungsionalitas drag and drop untuk area upload
 */
function setupDragAndDrop() {
    const uploadArea = document.getElementById('upload-area');
    if (!uploadArea) return;
    
    uploadArea.addEventListener('dragover', function(e) {
        e.preventDefault();
        this.style.border = '2px solid #0d6efd';
        this.style.backgroundColor = '#f0f8ff';
    });
    
    uploadArea.addEventListener('dragleave', function(e) {
        e.preventDefault();
        this.style.border = '2px dashed #ccc';
        this.style.backgroundColor = '';
    });
    
    uploadArea.addEventListener('drop', function(e) {
        e.preventDefault();
        
        const preview = document.getElementById('preview');
        const uploadContent = document.querySelector('.upload-content');
        const fileInput = document.getElementById('image');
        
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            fileInput.files = e.dataTransfer.files;
            showImagePreview(fileInput);
        }
    });
}

/**
 * Mengatur slider parameter filter dan menampilkan nilai
 */
function setupSliders() {
    // Domain Sigma Slider
    const domainSlider = document.getElementById('domain_sigma');
    if (domainSlider) {
        domainSlider.addEventListener('input', function() {
            updateSliderValue('domain_sigma_value', this.value);
        });
    }
    
    // Range Sigma Slider
    const rangeSlider = document.getElementById('range_sigma');
    if (rangeSlider) {
        rangeSlider.addEventListener('input', function() {
            updateSliderValue('range_sigma_value', this.value);
        });
    }
    
    // Offset Slider
    const offsetSlider = document.getElementById('offset');
    if (offsetSlider) {
        offsetSlider.addEventListener('input', function() {
            updateSliderValue('offset_value', this.value);
        });
    }
}

/**
 * Memperbarui tampilan nilai slider
 * @param {string} elementId - ID element yang menampilkan nilai
 * @param {string} value - Nilai yang akan ditampilkan
 */
function updateSliderValue(elementId, value) {
    const element = document.getElementById(elementId);
    if (element) {
        element.textContent = value;
    }
}

/**
 * Menampilkan perbandingan gambar sebelum dan sesudah pemrosesan
 * dengan animasi fade
 */
function showImageComparison() {
    const comparisons = document.querySelectorAll('.image-item');
    
    comparisons.forEach((item, index) => {
        setTimeout(() => {
            item.style.opacity = '1';
        }, index * 300);
    });
} 