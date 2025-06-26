// Dashboard JavaScript - WFP Comidas Escolares Ecuador

// Hide loading screen
window.addEventListener('load', () => {
    setTimeout(() => {
        document.getElementById('loading').classList.add('hide');
    }, 500);
});

// Animate numbers with formatting
const animateValue = (element, start, end, duration, decimals = 0) => {
    const startTimestamp = Date.now();
    const step = (timestamp) => {
        const progress = Math.min((Date.now() - startTimestamp) / duration, 1);
        const current = Math.floor(progress * (end - start) + start);
        
        if (decimals > 0) {
            element.textContent = current.toFixed(decimals).toLocaleString('es-EC');
        } else {
            element.textContent = current.toLocaleString('es-EC');
        }
        
        if (progress < 1) {
            window.requestAnimationFrame(step);
        }
    };
    window.requestAnimationFrame(step);
};

// Intersection Observer for animations
const observerOptions = {
    threshold: 0.5,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const element = entry.target;
            
            // Animate stat values
            if (element.classList.contains('stat-value')) {
                const endValue = parseFloat(element.getAttribute('data-count'));
                const decimals = parseInt(element.getAttribute('data-decimals') || '0');
                animateValue(element, 0, endValue, 2000, decimals);
            }
            
            observer.unobserve(element);
        }
    });
}, observerOptions);

// Observe all stat values
document.querySelectorAll('.stat-value').forEach(el => {
    observer.observe(el);
});

// Chart.js Configuration
Chart.defaults.font.family = "'Open Sans', sans-serif";
Chart.defaults.color = '#2f3237';

// Evolution Chart
const createEvolutionChart = () => {
    const ctx = document.getElementById('evolutionChart').getContext('2d');
    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, 'rgba(0, 51, 161, 0.3)');
    gradient.addColorStop(1, 'rgba(0, 51, 161, 0.05)');

    new Chart(ctx, {
        type: 'line',
        data: {
            labels: evolutionData.map(d => d.mes),
            datasets: [{
                label: 'Estudiantes Beneficiados',
                data: evolutionData.map(d => d.estudiantes),
                borderColor: '#0033a1',
                backgroundColor: gradient,
                borderWidth: 3,
                tension: 0.4,
                fill: true,
                pointBackgroundColor: '#0033a1',
                pointBorderColor: '#fff',
                pointBorderWidth: 2,
                pointRadius: 6,
                pointHoverRadius: 8
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    titleFont: {
                        size: 14,
                        weight: '600'
                    },
                    bodyFont: {
                        size: 13
                    },
                    callbacks: {
                        label: function(context) {
                            return 'Estudiantes: ' + context.parsed.y.toLocaleString('es-EC');
                        },
                        afterLabel: function(context) {
                            const dataIndex = context.dataIndex;
                            const ue = evolutionData[dataIndex].ue;
                            const tm = evolutionData[dataIndex].tm;
                            return [
                                'UE: ' + ue,
                                'TM Alimentos: ' + tm
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString('es-EC');
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
};

// Provincial Chart
const createProvincialChart = () => {
    const ctx = document.getElementById('provincialChart').getContext('2d');
    const provincialLabels = Object.keys(provincialData);
    const provincialValues = provincialLabels.map(p => provincialData[p].estudiantes);
    const provincialColors = provincialLabels.map(p => provincialData[p].color);
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: provincialLabels,
            datasets: [{
                label: 'Estudiantes por Provincia',
                data: provincialValues,
                backgroundColor: provincialColors,
                borderRadius: 8,
                barThickness: 40
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const provincia = context.label;
                            const estudiantes = context.parsed.y;
                            const ue = provincialData[provincia].ue;
                            return [
                                'Estudiantes: ' + estudiantes.toLocaleString('es-EC'),
                                'UE: ' + ue
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value.toLocaleString('es-EC');
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    },
                    ticks: {
                        autoSkip: false,
                        maxRotation: 45,
                        minRotation: 45
                    }
                }
            },
            onHover: (event, activeElements) => {
                event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
            }
        }
    });
};

// Modalidades Chart (Donut)
const createModalidadesChart = () => {
    const ctx = document.getElementById('modalidadesChart').getContext('2d');
    const total = modalidadesData.GAD + modalidadesData.MINEDUC;
    
    // Create center text plugin
    const centerTextPlugin = {
        id: 'centerText',
        beforeDraw: function(chart) {
            const width = chart.width;
            const height = chart.height;
            const ctx = chart.ctx;
            
            ctx.restore();
            const fontSize = (height / 160).toFixed(2);
            ctx.font = fontSize + "em Open Sans";
            ctx.textBaseline = "middle";
            ctx.fillStyle = "#2f3237";
            
            const text = total.toLocaleString('es-EC');
            const textX = Math.round((width - ctx.measureText(text).width) / 2);
            const textY = height / 2 - 10;
            
            ctx.fillText(text, textX, textY);
            
            ctx.font = (fontSize * 0.6) + "em Open Sans";
            ctx.fillStyle = "#5e636e";
            const subtext = "Total Estudiantes";
            const subtextX = Math.round((width - ctx.measureText(subtext).width) / 2);
            const subtextY = height / 2 + 10;
            
            ctx.fillText(subtext, subtextX, subtextY);
            ctx.save();
        }
    };
    
    new Chart(ctx, {
        type: 'doughnut',
        plugins: [centerTextPlugin],
        data: {
            labels: ['Modalidad GAD', 'Modalidad MINEDUC'],
            datasets: [{
                data: [modalidadesData.GAD, modalidadesData.MINEDUC],
                backgroundColor: ['#0033a1', '#FF6B00'],
                borderWidth: 0,
                spacing: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            cutout: '70%',
            plugins: {
                legend: {
                    position: 'bottom',
                    padding: 20,
                    labels: {
                        padding: 20,
                        font: {
                            size: 14,
                            weight: '600'
                        },
                        generateLabels: function(chart) {
                            const data = chart.data;
                            if (data.labels.length && data.datasets.length) {
                                return data.labels.map((label, i) => {
                                    const value = data.datasets[0].data[i];
                                    const percentage = ((value / total) * 100).toFixed(1);
                                    return {
                                        text: `${label}: ${value.toLocaleString('es-EC')} (${percentage}%)`,
                                        fillStyle: data.datasets[0].backgroundColor[i],
                                        hidden: false,
                                        index: i
                                    };
                                });
                            }
                            return [];
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            const percentage = ((value / total) * 100).toFixed(1);
                            return label + ': ' + value.toLocaleString('es-EC') + ' (' + percentage + '%)';
                        }
                    }
                }
            },
            onHover: (event, activeElements) => {
                event.native.target.style.cursor = activeElements.length > 0 ? 'pointer' : 'default';
            }
        }
    });
};

// Initialize all charts and map
document.addEventListener('DOMContentLoaded', () => {
    // Create charts with delay for smooth loading
    setTimeout(createEvolutionChart, 100);
    setTimeout(createProducersChart, 200);
    setTimeout(createModalidadesChart, 300);
    setTimeout(createFoodCategoriesChart, 400);
    setTimeout(initializeMap, 500);
    
    // Add hover effects to cards
    addCardHoverEffects();
    
    // Initialize smooth scroll
    initSmoothScroll();
});

// Producers Chart
const createProducersChart = () => {
    const ctx = document.getElementById('producersChart').getContext('2d');
    const producersInfo = productoresData.por_tamano;
    
    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['Pequeños\nProductores', 'Medianos\nProductores', 'Grandes\nProductores'],
            datasets: [{
                label: 'Cantidad de Productores',
                data: [
                    producersInfo.pequenos.cantidad,
                    producersInfo.medianos.cantidad,
                    producersInfo.grandes.cantidad
                ],
                backgroundColor: ['#228B22', '#0033a1', '#5e636e'],
                borderRadius: 8,
                barThickness: 60
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const types = ['pequenos', 'medianos', 'grandes'];
                            const type = types[index];
                            const info = producersInfo[type];
                            return [
                                'Cantidad: ' + info.cantidad,
                                'Porcentaje: ' + info.porcentaje + '%',
                                'Hectáreas promedio: ' + info.hectareas_promedio + ' ha'
                            ];
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: {
                        color: 'rgba(0, 0, 0, 0.05)'
                    },
                    ticks: {
                        callback: function(value) {
                            return value;
                        }
                    }
                },
                x: {
                    grid: {
                        display: false
                    }
                }
            }
        }
    });
};

// Food Categories Chart
const createFoodCategoriesChart = () => {
    const ctx = document.getElementById('foodCategoriesChart').getContext('2d');
    const labels = [];
    const data = [];
    const colors = [];
    
    for (const [key, categoria] of Object.entries(categoriasAlimentos)) {
        labels.push(categoria.nombre);
        data.push(categoria.porcentaje);
        colors.push(categoria.color);
    }
    
    new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: labels,
            datasets: [{
                data: data,
                backgroundColor: colors,
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: true,
            cutout: '60%',
            plugins: {
                legend: {
                    position: 'bottom',
                    padding: 20,
                    labels: {
                        padding: 15,
                        font: {
                            size: 12
                        }
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(0, 0, 0, 0.8)',
                    padding: 12,
                    cornerRadius: 8,
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.parsed;
                            return label + ': ' + value + '%';
                        }
                    }
                }
            }
        }
    });
};

// Initialize Ecuador Map
const initializeMap = () => {
    // Create map centered on Ecuador
    const map = L.map('ecuadorMap').setView([-1.831239, -78.183406], 7);
    
    // Add base map layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '© OpenStreetMap contributors',
        maxZoom: 19
    }).addTo(map);
    
    // Function to determine marker color based on student count
    const getMarkerColor = (students) => {
        if (students <= 1000) return '#FF6B00';
        if (students <= 3000) return '#007DBC';
        return '#0033a1';
    };
    
    // Add markers for each province
    for (const [provincia, data] of Object.entries(mapaCoordenadasData)) {
        const color = getMarkerColor(data.estudiantes);
        
        // Create custom icon
        const customIcon = L.divIcon({
            className: 'custom-marker',
            html: `<div style="background-color: ${color}; width: 40px; height: 40px; border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">${Math.round(data.estudiantes/100)}</div>`,
            iconSize: [40, 40],
            iconAnchor: [20, 20]
        });
        
        // Create marker
        const marker = L.marker([data.lat, data.lng], { icon: customIcon })
            .addTo(map)
            .bindPopup(`
                <div style="padding: 10px;">
                    <h4 style="margin: 0 0 10px 0; color: #0033a1;">${provincia}</h4>
                    <p style="margin: 5px 0;"><strong>Estudiantes:</strong> ${data.estudiantes.toLocaleString('es-EC')}</p>
                    <p style="margin: 5px 0;"><strong>Unidades Educativas:</strong> ${provincialData[provincia]?.ue || 'N/A'}</p>
                </div>
            `);
        
        // Add circle overlay for visual impact
        L.circle([data.lat, data.lng], {
            color: color,
            fillColor: color,
            fillOpacity: 0.2,
            radius: Math.sqrt(data.estudiantes) * 300,
            weight: 2
        }).addTo(map);
    }
    
    // Add Ecuador borders (simplified)
    const ecuadorBounds = [
        [-5.0, -81.0],
        [-5.0, -75.2],
        [1.5, -75.2],
        [1.5, -81.0]
    ];
    
    L.rectangle(ecuadorBounds, {
        color: "#0033a1",
        weight: 2,
        fill: false,
        dashArray: '5, 10'
    }).addTo(map);
};

// Card hover effects
const addCardHoverEffects = () => {
    document.querySelectorAll('.info-card li').forEach(li => {
        li.addEventListener('mouseenter', function() {
            this.style.transform = 'translateX(10px)';
        });
        li.addEventListener('mouseleave', function() {
            this.style.transform = 'translateX(0)';
        });
    });
};

// Smooth scroll for anchor links
const initSmoothScroll = () => {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
};

// Print functionality
window.addEventListener('beforeprint', () => {
    // Expand all charts for printing
    document.querySelectorAll('canvas').forEach(canvas => {
        canvas.style.maxHeight = 'none';
    });
});

window.addEventListener('afterprint', () => {
    // Restore chart sizes
    document.getElementById('modalidadesChart').style.maxHeight = '300px';
});

// Export notification
document.querySelectorAll('.export-btn').forEach(btn => {
    btn.addEventListener('click', function(e) {
        // Show temporary notification
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #0033a1;
            color: white;
            padding: 1rem 2rem;
            border-radius: 8px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 1000;
            animation: slideInUp 0.5s ease;
        `;
        notification.textContent = 'Generando archivo...';
        document.body.appendChild(notification);
        
        setTimeout(() => {
            notification.remove();
        }, 3000);
    });
});