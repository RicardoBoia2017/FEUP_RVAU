using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class GameManager : MonoBehaviour
{
    public GameObject enemyPrefab;
    private int numberEnemies = 0;
    private int maxEnemies = 15;
    private Text text;
    private GameObject hero;
    private bool invokerCalled = false;

    void Start()
    {
        text = GameObject.Find("Distance").GetComponent<Text>();
    }

    public void InvokeSpawnEnemy()
    {
        if(!invokerCalled)
        {
            hero =  GameObject.Find("Hero"); 
            InvokeRepeating("SpawnEnemy", 3f, 1f);
        }
    }

    void SpawnEnemy()
    {
        numberEnemies++;
        if(numberEnemies > maxEnemies)
            return;

        Transform enemyTransform;

        enemyTransform = enemyPrefab.transform;

/*        Vector3 origin = hero.transform.position; 
        float radius = 1f;

        Vector2 randomPos = Random.insideUnitCircle.normalized * radius;
        enemyTransform.position = origin + new Vector3(randomPos.x, 0, randomPos.y);


        enemyTransform.name = "Enemy #" + numberEnemies;
        Instantiate(enemyPrefab, enemyTransform);*/

/*      Make cubes spawn in front of hero*/
        
        Vector3 playerPos = hero.transform.position;
        Vector3 playerDirection = hero.transform.forward;
        Quaternion playerRotation = hero.transform.rotation;
        float spawnDistance = 1;

        Vector3 enemyPos = playerPos + playerDirection*spawnDistance;

        Instantiate(enemyPrefab, enemyPos, playerRotation);
    }

    public void GameOver(string name)
    {
        numberEnemies = maxEnemies;
        text.text = "Collided with " + name;
        GameObject[] enemies = GameObject.FindGameObjectsWithTag("Enemy");
        foreach (GameObject enemy in enemies)
            Destroy(enemy);
    }
}
