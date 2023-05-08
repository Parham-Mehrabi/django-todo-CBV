{% extends "mail_templated/base.tpl" %}

{% block subject %}
Account activation
{% endblock %}

{% block html %}
<p>click the link below to verify your account in</p><h3>parham-webdev.com</h3>
<h4>
    <a href="http://127.0.0.1:8000/auth/api/v1/activation/confirm/{{ token }}"> verify</a>
</h4>
<hr>
<img src="https://http.cat/200">
{% endblock %}
