(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){'use strict';var data=startQueue();Promise.resolve(data).then(function(data){document.getElementById('player-id').value=data['p1'];console.log(JSON.stringify(data));navigateToGame();});var delay=10000;var timerId=setTimeout(function request(){try{var p2_user_id=refreshQueue();Promise.resolve(p2_user_id).then(function(p2_user_id){console.log("Im here");var p2_id=p2_user_id;if(p2_id.ready){document.getElementById('game-id').value=p2_user_id['game-id'];console.log("WOOOOOOO");window.location='./game/'+p2_id['game-id'];}else if(!p2_id.ready){console.log("Not ready");var data=startQueue();Promise.resolve(data).then(function(data){if(data.ready){document.getElementById('player-id').value=data['p1'];console.log(JSON.stringify(data));navigateToGame();}});}});}catch(error){console.log(error);delay*=2;}
timerId=setTimeout(request,delay);},delay);async function refreshQueue(){var id=document.getElementById('player-id').value;var response=await fetch("http://localhost:9696/queue",{method:"POST",headers:{'Content-Type':'application/json'},body:JSON.stringify({"player_id":id,"size":2})});return response.json();}
async function startQueue(){var id=document.getElementById('player-id').value;var response=await fetch("http://localhost:9696/enqueue",{method:"POST",headers:{'Content-Type':'application/json'},body:JSON.stringify({"player_id":id,"size":2})});return response.json();}
async function navigateToGame(){var id=document.getElementById('player-id').value;document.sbmt.submit();}},{}]},{},[1]);;