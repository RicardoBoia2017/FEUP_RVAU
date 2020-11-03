using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class MineBehaviour : MonoBehaviour
{
    
    void OnCollisionEnter(Collision c)
    {
        if(c.collider.gameObject.transform.tag == "Enemy")
            Explode(c.collider.gameObject);
    }

    void Explode(GameObject collider) {
        Destroy(collider);
        ParticleSystem exp = GetComponent<ParticleSystem>();
        exp.Play();
        Destroy(gameObject, 0.25f);
    }
}
