document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);
  document.querySelector('form').onsubmit = send_email
  // By default, load the inbox
  load_mailbox('inbox');

});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#open_emails').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  document.querySelector('#emails').innerHTML = ''
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#emails').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#open_emails').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
    .then(response => response.json())
    .then(emails => {
        let emails_data = emails;
        console.log(emails_data);
        for (email in emails_data){
          let container = document.createElement('div');
          container.innerHTML = `<b>From</b>: ${emails_data[email].sender} <b>Subject</b>: ${emails_data[email].subject} <p style = "float: right">${emails_data[email].timestamp}</p>`;
          container.style.cssText = 'border : 1px solid black; margin-top: 10px; padding: 10px';
          let id = emails_data[email].id
          container.addEventListener('click', () => view_email(id));
          if (emails_data[email].read === true){
              container.style.background = 'lightgrey';
          }
          document.querySelector('#emails').append(container);

        }
    });
}

function view_email(id){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#open_emails').style.display = 'block';
  document.querySelector('#open_emails').innerHTML = ''

  fetch(`/emails/${id}`)
  .then(response => response.json())
  .then(email => {

      let sender = document.createElement('div');
      sender.innerHTML = `<b>From:</b><p style = "margin-left: 15px; display: inline">${email.sender}</p>`;
      sender.style.cssText = 'font-size: 25px;';
      document.querySelector('#open_emails').append(sender);


      let p = document.createElement('p');
      p.innerHTML = 'Recipients:';
      p.style.cssText = 'font-weight: bold; font-size: 25px; margin-bottom: 0px; display: inline';
      document.querySelector('#open_emails').append(p);
      for(recipient in email.recipients){
          let r = document.createElement('div');
          r.innerHTML = `${email.recipients[recipient]}`
          r.style.cssText = 'font-size: 25px; display: inline; margin-left: 15px'
          document.querySelector('#open_emails').append(r);
      }

      let subject = document.createElement('div');
      subject.innerHTML = `<b>Subject:</b><p style = "margin-left: 15px; display: inline">${email.subject}</p>`;
      subject.style.cssText = 'font-size: 25px;';
      document.querySelector('#open_emails').append(subject);

      let time = document.createElement('div');
      time.innerHTML = `<b>Time:</b><p style = "margin-left: 15px; display: inline">${email.timestamp}</p>`;
      time.style.cssText = 'font-size: 25px;';
      document.querySelector('#open_emails').append(time);

      let body = document.createElement('div');
      body.innerHTML = `<b>Body:</b><p style = "margin-left: 15px;">${email.body}</p>`;
      body.style.cssText = 'font-size: 25px;';
      document.querySelector('#open_emails').append(body);

      let div2 = document.createElement('div');
      div2.className = "button-group"
      document.querySelector('#open_emails').append(div2)

      let archive = document.createElement('button');
      
        if (email.archived === false){
          archive.className = "btn btn-sm btn-outline-primary";
          archive.innerHTML = "Archive";
          div2.append(archive);
          archive.addEventListener('click', () => {
            fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                  archived: true
              })
            })
            
            document.querySelector('#emails').innerHTML = ''
            load_mailbox('inbox');
          })
        }
        else{
          archive.className = "btn btn-sm btn-outline-primary";
          archive.innerHTML = "Unarchive";
          div2.append(archive);
          archive.addEventListener('click', () => {
            fetch(`/emails/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                  archived: false
              })
            })
            
            document.querySelector('#emails').innerHTML = ''
            load_mailbox('inbox');
          })
        }

      let reply = document.createElement('button');
      reply.className = "btn btn-sm btn-outline-primary";
      reply.innerHTML = "Reply";
      reply.style.cssText = "margin-left: 15px;"
      div2.append(reply)
      reply.addEventListener('click', () => reply_email(email.sender, email.subject, email.timestamp, email.body));
  })

  fetch(`/emails/${id}`, {
  method: 'PUT',
  body: JSON.stringify({
        read: true
    })
  })
}

function reply_email(sender, subject, time, body){
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#emails').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#open_emails').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';


  document.querySelector('#title').innerHTML = 'Reply'

  let to = document.querySelector('#compose-recipients')
  to.value = sender;
  to.disabled = true;

  let re = subject.slice(0, 2);
  match = `${re}`.localeCompare('Re');
  let re_subject = document.querySelector('#compose-subject')
  if (match == 0){
    re_subject.value = subject
  }
  else{
    re_subject.value = `Re: ${subject}`
  }
  
  let re_body = document.querySelector('#compose-body')
  re_body.value = `On ${time} ${sender} Wrote:\n${body}` 

}

function send_email() {
  fetch('/emails', {
  method: 'POST',
  body: JSON.stringify({
      recipients: document.querySelector('#compose-recipients').value,
      subject: document.querySelector('#compose-subject').value,
      body: document.querySelector('#compose-body').value
    })
  })
  .then(response => response.json())
  .then(result => {
      console.log(result);
  })
  .then(load_mailbox('sent'));
  return false;
}
