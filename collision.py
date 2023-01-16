def handleBoxCollision(particle, box):
    if particle.left <= box.left or particle.right >= box.right:
        particle.velocity.x *= -1
    if particle.bottom >= box.bottom or particle.top <= box.top:
        particle.velocity.y *= -1
