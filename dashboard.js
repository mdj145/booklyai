async function createAppointment(e){
  e.preventDefault();
  const payload = {
    customer_name: document.getElementById('customer_name').value,
    customer_phone: document.getElementById('customer_phone').value,
    start_time: new Date(document.getElementById('start_time').value).toISOString(),
    end_time: new Date(document.getElementById('end_time').value).toISOString(),
    notes: document.getElementById('notes').value,
    reminder_24h: document.getElementById('rem24').checked,
    reminder_1h: document.getElementById('rem1').checked
  };
  const res = await fetch('/api/appointments', {
    method:'POST',
    headers:{ 'Content-Type':'application/json' },
    body: JSON.stringify(payload)
  });
  if(!res.ok){ alert('Failed to create'); return; }
  await loadAppointments();
  e.target.reset();
}

async function loadAppointments(){
  const res = await fetch('/api/appointments');
  const data = await res.json();
  const tbody = document.querySelector('#appt-table tbody');
  tbody.innerHTML = '';
  data.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td>${row.id}</td>
      <td>${row.customer_name}</td>
      <td>${row.customer_phone}</td>
      <td>${new Date(row.start_time).toLocaleString()}</td>
      <td>${new Date(row.end_time).toLocaleString()}</td>
      <td><button onclick="del(${row.id})">Delete</button></td>`;
    tbody.appendChild(tr);
  });
}

async function del(id){
  const res = await fetch('/api/appointments/' + id, { method:'DELETE' });
  if(!res.ok){ alert('Failed to delete'); return; }
  await loadAppointments();
}

document.getElementById('appt-form').addEventListener('submit', createAppointment);
loadAppointments();
